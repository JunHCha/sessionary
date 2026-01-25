<script lang="ts" module>
	import { PLAYBACK_SPEEDS, formatTime } from '../utils'

	/**
	 * 다음 재생 속도 반환 (순환)
	 */
	export function getNextPlaybackSpeed(currentSpeed: number): number {
		const index = PLAYBACK_SPEEDS.indexOf(currentSpeed as (typeof PLAYBACK_SPEEDS)[number])
		if (index === -1) return 1.0
		return PLAYBACK_SPEEDS[(index + 1) % PLAYBACK_SPEEDS.length]
	}

	/**
	 * 재생 속도를 "Nx" 형식으로 포맷
	 */
	export function formatPlaybackSpeed(speed: number): string {
		if (speed === 1) return '1x'
		return `${speed}x`
	}

	/**
	 * 진행률 계산 (0-100)
	 */
	export function calculateProgress(currentTime: number, duration: number): number {
		if (!duration || isNaN(duration) || duration === 0) return 0
		return (currentTime / duration) * 100
	}
</script>

<script lang="ts">
	import { onDestroy } from 'svelte'

	let { videoElement }: { videoElement: HTMLVideoElement | undefined } = $props()

	let isPlaying = $state(false)
	let currentTime = $state(0)
	let duration = $state(0)
	let volume = $state(1)
	let isMuted = $state(false)
	let playbackSpeed = $state(1.0)
	let isLooping = $state(false)
	let showControls = $state(true)

	let hideControlsTimer: ReturnType<typeof setTimeout> | null = null

	onDestroy(() => {
		if (hideControlsTimer) clearTimeout(hideControlsTimer)
	})

	function togglePlay() {
		if (!videoElement) return
		if (videoElement.paused) {
			videoElement.play()
		} else {
			videoElement.pause()
		}
	}

	function toggleMute() {
		if (!videoElement) return
		videoElement.muted = !videoElement.muted
		isMuted = videoElement.muted
	}

	function changeVolume(e: Event) {
		if (!videoElement) return
		const target = e.target as HTMLInputElement
		const newVolume = parseFloat(target.value)
		videoElement.volume = newVolume
		volume = newVolume
		isMuted = newVolume === 0
	}

	function seek(e: MouseEvent) {
		if (!videoElement || !duration) return
		const target = e.currentTarget as HTMLElement
		const rect = target.getBoundingClientRect()
		const percent = (e.clientX - rect.left) / rect.width
		videoElement.currentTime = percent * duration
	}

	function cyclePlaybackSpeed() {
		if (!videoElement) return
		playbackSpeed = getNextPlaybackSpeed(playbackSpeed)
		videoElement.playbackRate = playbackSpeed
	}

	function toggleLoop() {
		if (!videoElement) return
		isLooping = !isLooping
		videoElement.loop = isLooping
	}

	function toggleFullscreen() {
		if (!videoElement) return
		const container = videoElement.closest('div')
		if (!container) return

		if (document.fullscreenElement) {
			document.exitFullscreen()
		} else {
			container.requestFullscreen()
		}
	}

	function handleMouseMove() {
		showControls = true
		if (hideControlsTimer) clearTimeout(hideControlsTimer)
		hideControlsTimer = setTimeout(() => {
			if (isPlaying) showControls = false
		}, 3000)
	}

	// Video element 이벤트 리스너 동기화
	$effect(() => {
		if (!videoElement) return

		const handleTimeUpdate = () => {
			currentTime = videoElement.currentTime
			duration = videoElement.duration || 0
		}

		const handlePlayState = () => {
			isPlaying = !videoElement.paused
		}

		videoElement.addEventListener('timeupdate', handleTimeUpdate)
		videoElement.addEventListener('play', handlePlayState)
		videoElement.addEventListener('pause', handlePlayState)
		videoElement.addEventListener('loadedmetadata', handleTimeUpdate)

		return () => {
			videoElement.removeEventListener('timeupdate', handleTimeUpdate)
			videoElement.removeEventListener('play', handlePlayState)
			videoElement.removeEventListener('pause', handlePlayState)
			videoElement.removeEventListener('loadedmetadata', handleTimeUpdate)
		}
	})
</script>

<div
	class="absolute inset-0"
	role="region"
	aria-label="Video controls"
	onmousemove={handleMouseMove}
	onmouseleave={() => {
		if (isPlaying) showControls = false
	}}
>
	<!-- Play/Pause overlay -->
	<button
		class="absolute inset-0 w-full h-full cursor-pointer bg-transparent"
		onclick={togglePlay}
		aria-label={isPlaying ? 'Pause' : 'Play'}
	>
	</button>

	<!-- Controls bar -->
	<div
		class="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent transition-opacity duration-300 {!showControls ? 'opacity-0 pointer-events-none' : ''}"
	>
		<!-- Progress bar -->
		<div
			class="w-full h-1 bg-white/30 rounded-full mb-3 cursor-pointer group"
			role="slider"
			aria-label="Seek"
			aria-valuemin={0}
			aria-valuemax={100}
			aria-valuenow={calculateProgress(currentTime, duration)}
			tabindex={0}
			onclick={seek}
			onkeydown={(e) => {
				if (!videoElement) return
				if (e.key === 'ArrowRight') {
					e.preventDefault()
					videoElement.currentTime += 5
				}
				if (e.key === 'ArrowLeft') {
					e.preventDefault()
					videoElement.currentTime -= 5
				}
			}}
		>
			<div
				class="h-full bg-white rounded-full relative"
				style="width: {calculateProgress(currentTime, duration)}%"
			>
				<div
					class="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
				></div>
			</div>
		</div>

		<!-- Controls row -->
		<div class="flex items-center justify-between text-white">
			<div class="flex items-center gap-4">
				<!-- Play/Pause button -->
				<button onclick={togglePlay} aria-label={isPlaying ? 'Pause' : 'Play'} class="p-1">
					{#if isPlaying}
						<svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
							<path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
						</svg>
					{:else}
						<svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
							<path d="M8 5v14l11-7z" />
						</svg>
					{/if}
				</button>

				<!-- Volume -->
				<div class="flex items-center gap-2">
					<button onclick={toggleMute} aria-label={isMuted ? 'Unmute' : 'Mute'} class="p-1">
						{#if isMuted || volume === 0}
							<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
								<path
									d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"
								/>
							</svg>
						{:else}
							<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
								<path
									d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
								/>
							</svg>
						{/if}
					</button>
					<input
						type="range"
						min="0"
						max="1"
						step="0.1"
						value={isMuted ? 0 : volume}
						oninput={changeVolume}
						class="w-16 h-1 bg-white/30 rounded-full appearance-none cursor-pointer"
						aria-label="Volume"
					/>
				</div>

				<!-- Time display -->
				<span class="text-sm tabular-nums">
					{formatTime(currentTime)} / {formatTime(duration)}
				</span>
			</div>

			<div class="flex items-center gap-3">
				<!-- Playback speed -->
				<button
					onclick={cyclePlaybackSpeed}
					class="px-2 py-1 text-sm font-medium hover:bg-white/20 rounded"
					aria-label="Playback speed"
				>
					{formatPlaybackSpeed(playbackSpeed)}
				</button>

				<!-- Loop toggle -->
				<button
					onclick={toggleLoop}
					class="p-1 rounded {isLooping ? 'bg-white/20' : ''}"
					aria-label={isLooping ? 'Disable loop' : 'Enable loop'}
					aria-pressed={isLooping}
				>
					<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"
						/>
					</svg>
				</button>

				<!-- Fullscreen -->
				<button onclick={toggleFullscreen} class="p-1" aria-label="Toggle fullscreen">
					<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
						/>
					</svg>
				</button>
			</div>
		</div>
	</div>
</div>
