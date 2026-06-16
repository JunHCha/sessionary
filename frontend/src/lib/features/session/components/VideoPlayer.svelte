<script lang="ts" module>
	import { isHlsSource } from '../utils'

	/**
	 * 기본 Props 값 반환 (테스트용)
	 */
	export function getDefaultProps() {
		return {
			autoplay: false,
			poster: undefined
		}
	}

	/**
	 * hls.js 사용 여부 판단
	 * @param src 비디오 소스 URL
	 * @param nativeHlsSupport 브라우저 네이티브 HLS 지원 여부
	 * @param hlsJsSupported hls.js 라이브러리 지원 여부
	 */
	export function shouldUseHlsJs(
		src: string,
		nativeHlsSupport: boolean,
		hlsJsSupported: boolean
	): boolean {
		if (!isHlsSource(src)) return false
		if (nativeHlsSupport) return false
		return hlsJsSupported
	}

	/**
	 * video 요소에 설정할 src 결정
	 * HLS 소스인데 네이티브 미지원 시 빈 문자열 (hls.js가 처리)
	 */
	export function getVideoSource(src: string, nativeHlsSupport: boolean): string {
		if (isHlsSource(src) && !nativeHlsSupport) {
			return ''
		}
		return src
	}

	/**
	 * 로딩 스피너 해제 여부 판단
	 * iOS Safari는 사용자 제스처 전까지 canplay를 발생시키지 않으므로
	 * loadedmetadata 시점에도 로딩을 해제한다
	 */
	export function shouldClearLoading(eventType: 'canplay' | 'loadedmetadata'): boolean {
		return eventType === 'canplay' || eventType === 'loadedmetadata'
	}

	/**
	 * 자동재생 시 음소거로 시작해야 하는지 판단
	 * 브라우저는 소리 있는 자동재생을 차단하므로 autoplay면 음소거로 시작한다
	 */
	export function shouldStartMuted(autoplay: boolean): boolean {
		return autoplay
	}

	/**
	 * "탭하여 소리 켜기" 어포던스 표시 여부 판단
	 * 자동재생 음소거 중이고 에러가 없을 때만 표시 (에러 오버레이가 우선)
	 */
	export function shouldShowUnmuteAffordance(
		autoplay: boolean,
		muted: boolean,
		hasError: boolean
	): boolean {
		return autoplay && muted && !hasError
	}

	/**
	 * 스피너 오버레이 클래스
	 * pointer-events-none: 스피너가 떠 있어도 아래 VideoControls 탭이 가능해야 함 (iOS 데드락 방지)
	 */
	export const SPINNER_OVERLAY_CLASS =
		'absolute inset-0 flex items-center justify-center bg-black/50 z-10 pointer-events-none'
</script>

<script lang="ts">
	import Hls from 'hls.js'
	import { onDestroy } from 'svelte'
	import type { VideoPlayerProps, TimeUpdateEvent, ErrorEvent, SeekRequest } from '../types'
	import VideoControls from './VideoControls.svelte'

	let {
		src,
		poster = undefined,
		autoplay = false,
		seekTo = undefined,
		ontimeupdate,
		onplay,
		onpause,
		onended,
		onerror
	}: VideoPlayerProps & {
		seekTo?: SeekRequest
		ontimeupdate?: (event: TimeUpdateEvent) => void
		onplay?: () => void
		onpause?: () => void
		onended?: () => void
		onerror?: (event: ErrorEvent) => void
	} = $props()

	let videoElement: HTMLVideoElement
	let hls: Hls | null = null
	let isLoading = $state(true)
	let errorMessage = $state<string | null>(null)
	// autoplay는 세션 동안 변하지 않는 prop이므로 초기값 캡처가 의도된 동작
	// svelte-ignore state_referenced_locally
	let muted = $state(shouldStartMuted(autoplay))

	let showUnmuteAffordance = $derived(
		shouldShowUnmuteAffordance(autoplay, muted, errorMessage !== null)
	)

	function unmute() {
		muted = false
		if (videoElement) videoElement.muted = false
	}

	// 브라우저 환경 체크
	const isBrowser = typeof window !== 'undefined'
	const nativeHlsSupport = isBrowser
		? document.createElement('video').canPlayType('application/vnd.apple.mpegurl') !== ''
		: false
	const hlsJsSupported = isBrowser ? Hls.isSupported() : false

	function handleTimeUpdate() {
		if (videoElement && ontimeupdate) {
			ontimeupdate({
				currentTime: videoElement.currentTime,
				duration: videoElement.duration || 0
			})
		}
	}

	function handlePlay() {
		onplay?.()
	}

	function handlePause() {
		onpause?.()
	}

	function handleEnded() {
		onended?.()
	}

	function handleError(message: string) {
		errorMessage = message
		isLoading = false
		onerror?.({ message })
	}

	function handleCanPlay() {
		if (shouldClearLoading('canplay')) {
			isLoading = false
			errorMessage = null
		}
	}

	function handleLoadedMetadata() {
		if (shouldClearLoading('loadedmetadata')) {
			isLoading = false
			errorMessage = null
		}
	}

	function initHls() {
		if (!videoElement || !src) return

		if (shouldUseHlsJs(src, nativeHlsSupport, hlsJsSupported)) {
			hls = new Hls()
			hls.loadSource(src)
			hls.attachMedia(videoElement)

			hls.on(Hls.Events.MANIFEST_PARSED, () => {
				if (autoplay) {
					videoElement.muted = muted
					videoElement.play().catch(() => {})
				}
			})

			hls.on(Hls.Events.ERROR, (_, data) => {
				if (data.fatal) {
					handleError(data.details || 'HLS playback error')
				}
			})
		} else if (autoplay && videoElement.src) {
			videoElement.muted = muted
			videoElement.play().catch(() => {})
		}
	}

	function destroyHls() {
		if (hls) {
			hls.destroy()
			hls = null
		}
	}

	onDestroy(() => {
		destroyHls()
	})

	// src 변경 시 재초기화
	$effect(() => {
		if (src && videoElement) {
			destroyHls()
			isLoading = true
			errorMessage = null
			initHls()
		}
	})

	let lastSeekVersion = -1

	$effect(() => {
		if (seekTo && seekTo.version !== lastSeekVersion && videoElement) {
			videoElement.currentTime = seekTo.time
			lastSeekVersion = seekTo.version
		}
	})
</script>

<div data-testid="video-player" class="relative w-full aspect-video bg-black rounded-xl overflow-hidden">
	{#if isLoading}
		<div class={SPINNER_OVERLAY_CLASS}>
			<div class="w-12 h-12 border-4 border-white/30 border-t-white rounded-full animate-spin">
			</div>
		</div>
	{/if}

	{#if errorMessage}
		<div class="absolute inset-0 flex items-center justify-center bg-black/80 z-20">
			<div class="text-center text-white">
				<p class="text-lg mb-2">재생 오류</p>
				<p class="text-sm text-gray-400">{errorMessage}</p>
			</div>
		</div>
	{/if}

	<video
		bind:this={videoElement}
		class="w-full h-full object-contain"
		{poster}
		src={getVideoSource(src, nativeHlsSupport)}
		bind:muted={muted}
		playsinline
		preload="metadata"
		ontimeupdate={handleTimeUpdate}
		onplay={handlePlay}
		onpause={handlePause}
		onended={handleEnded}
		oncanplay={handleCanPlay}
		onloadedmetadata={handleLoadedMetadata}
		onerror={() => handleError('Failed to load video')}
	>
		<track kind="captions" />
	</video>

	<VideoControls {videoElement} />

	{#if showUnmuteAffordance}
		<button
			type="button"
			data-testid="unmute-affordance"
			onclick={unmute}
			class="absolute top-3 right-3 z-30 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/70 text-white text-sm font-medium backdrop-blur-sm hover:bg-black/80 transition-colors"
			aria-label="탭하여 소리 켜기"
		>
			<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
				<path
					d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"
				/>
			</svg>
			<span>탭하여 소리 켜기</span>
		</button>
	{/if}
</div>
