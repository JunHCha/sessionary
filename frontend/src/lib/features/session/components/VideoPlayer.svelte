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
</script>

<script lang="ts">
	import Hls from 'hls.js'
	import { onMount, onDestroy } from 'svelte'
	import type { VideoPlayerProps, TimeUpdateEvent, ErrorEvent } from '../types'
	import VideoControls from './VideoControls.svelte'

	let {
		src,
		poster = undefined,
		autoplay = false,
		ontimeupdate,
		onplay,
		onpause,
		onended,
		onerror
	}: VideoPlayerProps & {
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
		isLoading = false
		errorMessage = null
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

	onMount(() => {
		initHls()
	})

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
</script>

<div class="relative w-full aspect-video bg-black rounded-xl overflow-hidden">
	{#if isLoading}
		<div class="absolute inset-0 flex items-center justify-center bg-black/50 z-10">
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
		ontimeupdate={handleTimeUpdate}
		onplay={handlePlay}
		onpause={handlePause}
		onended={handleEnded}
		oncanplay={handleCanPlay}
		onerror={() => handleError('Failed to load video')}
	>
		<track kind="captions" />
	</video>

	<VideoControls {videoElement} />
</div>
