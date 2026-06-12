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
					videoElement.play().catch(() => {})
				}
			})

			hls.on(Hls.Events.ERROR, (_, data) => {
				if (data.fatal) {
					handleError(data.details || 'HLS playback error')
				}
			})
		} else if (autoplay && videoElement.src) {
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
</div>
