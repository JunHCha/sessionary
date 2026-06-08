<script lang="ts">
	import { goto } from '$app/navigation'
	import { waitForApiInit } from '$lib/api/config'
	import {
		VideoPlayer,
		SubtitleRoller,
		TabSheet,
		loadSessionDetail,
		type SessionDetailData,
		type SeekRequest
	} from '$lib/features/session'

	let { data } = $props()

	let session = $state<SessionDetailData | null>(null)
	let loading = $state(true)
	let error = $state<string | null>(null)
	let currentTime = $state(0)
	let seekRequest = $state<SeekRequest | undefined>(undefined)

	function handleSeekRequest(timeSec: number) {
		seekRequest = { time: timeSec, version: (seekRequest?.version ?? 0) + 1 }
	}

	let currentRequestId = 0

	async function fetchSession(sessionId: number) {
		const requestId = ++currentRequestId
		loading = true
		error = null
		session = null
		try {
			await waitForApiInit()
			const result = await loadSessionDetail(sessionId)
			if (requestId !== currentRequestId) return
			session = result
		} catch (e) {
			if (requestId !== currentRequestId) return
			error = e instanceof Error ? e.message : '세션을 불러올 수 없습니다'
		} finally {
			if (requestId === currentRequestId) loading = false
		}
	}

	$effect(() => {
		fetchSession(data.sessionId)
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
			<div data-testid="session-loading" class="flex items-center justify-center h-[60vh]">
				<div class="text-[#999] text-lg">로딩 중...</div>
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
					<VideoPlayer
						src={session.videoUrl}
						seekTo={seekRequest}
						ontimeupdate={(e) => (currentTime = e.currentTime)}
					/>
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
