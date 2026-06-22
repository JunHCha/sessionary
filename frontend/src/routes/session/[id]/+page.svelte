<script lang="ts">
	import Hls from 'hls.js'
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { waitForApiInit } from '$lib/api/config'
	import { OpenAPI } from '$lib/api/client'
	import {
		VideoPlayer,
		SubtitleRoller,
		TabSheet,
		SessionLoadingSplash,
		NextSessionCountdown,
		loadSessionDetail,
		reportLessonPosition,
		fetchLessonResumePosition,
		evaluatePositionReport,
		createReportState,
		buildPositionBeacon,
		MIN_SPLASH_MS,
		PRELOAD_TIMEOUT_MS,
		areResourcesReady,
		isVideoReady,
		shouldTransitionFromSplash,
		selectPreloadStrategy,
		shouldShowCountdown,
		type SessionDetailData,
		type SeekRequest,
		type ReportState
	} from '$lib/features/session'

	let { data } = $props()

	let session = $state<SessionDetailData | null>(null)
	let loading = $state(true)
	let error = $state<string | null>(null)
	let currentTime = $state(0)
	let seekRequest = $state<SeekRequest | undefined>(undefined)
	let showCountdown = $state(false)

	// 스플래시 게이트 상태
	let minElapsed = $state(false)
	let videoPreloaded = $state(false)

	function handleSeekRequest(timeSec: number) {
		seekRequest = { time: timeSec, version: (seekRequest?.version ?? 0) + 1 }
	}

	// --- 위치 리포팅 (비반응 상태: effect 자기참조 회귀 #125 방지) ---
	let reportState: ReportState = createReportState()
	let lastPosition = 0
	let lastDuration = 0

	function resetReporting() {
		reportState = createReportState()
		lastPosition = 0
		lastDuration = 0
	}

	function sendReport(positionSec: number, durationSec: number) {
		if (!session || durationSec <= 0) return
		void reportLessonPosition(session.id, positionSec, durationSec)
	}

	function handlePositionUpdate(time: number, duration: number) {
		currentTime = time
		lastPosition = time
		lastDuration = duration
		const decision = evaluatePositionReport(reportState, {
			currentTime: time,
			duration,
			now: Date.now()
		})
		reportState = { lastReportedAt: decision.lastReportedAt, fired90: decision.fired90 }
		if (decision.shouldReport) {
			sendReport(time, duration)
		}
	}

	function flushPosition(viaBeacon: boolean) {
		if (!session || lastDuration <= 0) return
		if (viaBeacon && typeof navigator !== 'undefined') {
			// PUT 전용 엔드포인트라 sendBeacon(POST) 대신 fetch keepalive 사용
			const beacon = buildPositionBeacon(OpenAPI.BASE, session.id, lastPosition, lastDuration)
			void fetch(beacon.url, {
				method: 'PUT',
				body: beacon.blob,
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				keepalive: true
			}).catch(() => {})
			return
		}
		sendReport(lastPosition, lastDuration)
	}

	async function applyResumeSeek(loaded: SessionDetailData) {
		const pos = await fetchLessonResumePosition(loaded.lectureId, loaded.id)
		if (pos > 0 && session?.id === loaded.id) {
			handleSeekRequest(pos)
		}
	}

	function handleVisibilityChange() {
		if (typeof document !== 'undefined' && document.visibilityState === 'hidden') {
			flushPosition(true)
		}
	}

	onMount(() => {
		if (typeof document === 'undefined') return
		document.addEventListener('visibilitychange', handleVisibilityChange)
		window.addEventListener('beforeunload', () => flushPosition(true))
		return () => {
			document.removeEventListener('visibilitychange', handleVisibilityChange)
		}
	})

	let currentRequestId = 0
	let minTimer: ReturnType<typeof setTimeout> | undefined
	let preloadTimer: ReturnType<typeof setTimeout> | undefined
	let preloadHls: Hls | null = null
	let preloadVideo: HTMLVideoElement | null = null

	function cleanupPreload() {
		clearTimeout(minTimer)
		clearTimeout(preloadTimer)
		if (preloadHls) {
			preloadHls.destroy()
			preloadHls = null
		}
		if (preloadVideo) {
			preloadVideo.removeAttribute('src')
			preloadVideo.load()
			preloadVideo = null
		}
	}

	// 데이터 도착 시 영상 prefetch 시작 (videoUrl 없으면 즉시 ready)
	function startVideoPreload(videoUrl: string, requestId: number) {
		const markReady = () => {
			if (requestId === currentRequestId) videoPreloaded = true
		}

		const strategy = selectPreloadStrategy(videoUrl)
		if (strategy === 'none') {
			markReady()
			return
		}

		// 안전장치: 프리로드 지연/실패해도 상한 시간 후 ready 처리
		preloadTimer = setTimeout(markReady, PRELOAD_TIMEOUT_MS)

		if (strategy === 'hls' && Hls.isSupported()) {
			preloadHls = new Hls()
			preloadHls.loadSource(videoUrl)
			preloadHls.on(Hls.Events.MANIFEST_PARSED, markReady)
			preloadHls.on(Hls.Events.ERROR, (_, d) => {
				if (d.fatal) markReady()
			})
		} else {
			preloadVideo = document.createElement('video')
			preloadVideo.preload = 'auto'
			preloadVideo.muted = true
			preloadVideo.addEventListener('loadedmetadata', markReady)
			preloadVideo.addEventListener('canplay', markReady)
			preloadVideo.addEventListener('error', markReady)
			preloadVideo.src = videoUrl
		}
	}

	async function fetchSession(sessionId: number) {
		const requestId = ++currentRequestId
		cleanupPreload()
		loading = true
		error = null
		session = null
		minElapsed = false
		videoPreloaded = false
		showCountdown = false
		seekRequest = undefined
		resetReporting()

		minTimer = setTimeout(() => {
			if (requestId === currentRequestId) minElapsed = true
		}, MIN_SPLASH_MS)

		try {
			await waitForApiInit()
			const result = await loadSessionDetail(sessionId)
			if (requestId !== currentRequestId) return
			session = result
			startVideoPreload(result.videoUrl, requestId)
			void applyResumeSeek(result)
		} catch (e) {
			if (requestId !== currentRequestId) return
			error = e instanceof Error ? e.message : '세션을 불러올 수 없습니다'
			loading = false
		}
	}

	// 리소스 준비 판정: 자막/악보는 데이터 동봉이므로 도착 시 ready
	const resourcesReady = $derived(
		!!session &&
			areResourcesReady({
				video: isVideoReady(session.videoUrl, videoPreloaded),
				subtitles: true,
				sheet: true
			})
	)

	// 전환 게이트: 최소 시간 경과 && 리소스 준비 시 스플래시 종료
	$effect(() => {
		if (error) return
		if (shouldTransitionFromSplash({ minElapsed, resourcesReady })) {
			loading = false
		}
	})

	$effect(() => {
		fetchSession(data.sessionId)
		return cleanupPreload
	})

	function goToPrevious() {
		if (session?.prevSessionId) {
			goto(`/session/${session.prevSessionId}`)
		}
	}

	function goToNext() {
		if (session?.nextSessionId) {
			goto(`/session/${session.nextSessionId}`)
		}
	}
</script>

<main data-testid="session-detail-page" class="min-h-screen bg-[#0c0c0c] pt-[73px] flex flex-col">
	<div class="w-full max-w-[1280px] min-w-[390px] mx-auto px-[40px] py-6 flex-1 flex flex-col">
		{#if loading}
			<div data-testid="session-loading">
				<SessionLoadingSplash />
			</div>
		{:else if error}
			<div data-testid="session-error" class="flex items-center justify-center h-[60vh]">
				<div class="text-red-400 text-lg">{error}</div>
			</div>
		{:else if session}
			<!-- 심플 헤더 -->
			<div class="flex items-end justify-between gap-4 mb-5">
				<h1 data-testid="session-title" class="text-2xl font-bold leading-tight text-white">
					{session.title}
				</h1>
				<div data-testid="session-progress" class="text-sm font-medium shrink-0">
					<span class="text-brand-primary"
						>{String(session.lectureOrdering).padStart(2, '0')}</span
					>
					<span class="text-[#666] mx-1.5">/</span>
					<span class="text-[#ddd]">{String(session.totalSessions).padStart(2, '0')}</span
					>
				</div>
			</div>

			<!-- Video + Subtitle Roller (세로 스택, 컨테이너 전체 너비) -->
			<div class="mb-4">
				{#if session.videoUrl}
					<div class="relative">
						<VideoPlayer
							src={session.videoUrl}
							seekTo={seekRequest}
							ontimeupdate={(e) => handlePositionUpdate(e.currentTime, e.duration)}
							onpause={() => flushPosition(false)}
							onended={() => {
								flushPosition(false)
								if (shouldShowCountdown(session?.nextSessionId))
									showCountdown = true
							}}
						/>
						{#if showCountdown && session.nextSessionId}
							<NextSessionCountdown
								nextSessionId={session.nextSessionId}
								nextSessionTitle={session.nextSessionTitle}
								nextOrdering={session.lectureOrdering + 1}
								onstart={goToNext}
								oncancel={() => (showCountdown = false)}
							/>
						{/if}
					</div>
				{:else}
					<div
						data-testid="video-unavailable"
						class="w-full aspect-video bg-black rounded-xl flex items-center justify-center"
					>
						<p class="text-[#666] text-sm">이 세션에는 영상이 제공되지 않습니다</p>
					</div>
				{/if}

				<div class="mt-3">
					<SubtitleRoller
						subtitles={session.subtitles}
						{currentTime}
						onseekrequest={handleSeekRequest}
					/>
				</div>
			</div>

			<!-- Tab Sheet (남은 높이를 채워 페이지 height full) -->
			<div class="mb-4 flex-1 flex">
				<TabSheet
					sheetmusicUrl={session.sheetmusicUrl}
					{currentTime}
					syncOffset={session.syncOffset}
				/>
			</div>

			<!-- Session Navigation -->
			<nav
				data-testid="session-navigation"
				class="flex items-center justify-center gap-8 py-4 bg-[#1a1a1a] rounded-lg"
			>
				<button
					type="button"
					onclick={goToPrevious}
					disabled={!session.prevSessionId}
					class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 19l-7-7 7-7"
						/>
					</svg>
					<span>이전 세션</span>
				</button>

				<div class="text-white font-medium">
					<span class="text-brand-primary"
						>{String(session.lectureOrdering).padStart(2, '0')}</span
					>
					<span class="text-[#666] mx-2">/</span>
					<span>{String(session.totalSessions).padStart(2, '0')}</span>
				</div>

				<button
					type="button"
					onclick={goToNext}
					disabled={!session.nextSessionId}
					class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					<span>다음 세션</span>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5l7 7-7 7"
						/>
					</svg>
				</button>
			</nav>
		{/if}
	</div>
</main>
