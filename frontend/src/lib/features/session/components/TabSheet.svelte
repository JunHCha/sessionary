<script lang="ts" module>
	export interface ExternalMediaHandlerOptions {
		videoDuration: number
		videoPlaybackRate: number
		videoVolume: number
		onSeek: (timeSec: number) => void
		onPlay: () => void
		onPause: () => void
	}

	export interface ExternalMediaHandler {
		readonly backingTrackDuration: number
		playbackRate: number
		masterVolume: number
		seekTo(time: number): void
		play(): void
		pause(): void
	}

	export function createExternalMediaHandler(
		options: ExternalMediaHandlerOptions
	): ExternalMediaHandler {
		return {
			get backingTrackDuration() {
				return options.videoDuration * 1000
			},
			get playbackRate() {
				return options.videoPlaybackRate
			},
			set playbackRate(v: number) {
				options.videoPlaybackRate = v
			},
			get masterVolume() {
				return options.videoVolume
			},
			set masterVolume(v: number) {
				options.videoVolume = v
			},
			seekTo(time: number) {
				options.onSeek(time / 1000)
			},
			play() {
				options.onPlay()
			},
			pause() {
				options.onPause()
			}
		}
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte'

	interface TabSheetProps {
		sheetmusicUrl: string | null
		currentTime: number
		syncOffset: number
	}

	let { sheetmusicUrl, currentTime, syncOffset }: TabSheetProps = $props()

	let containerEl: HTMLDivElement | undefined = $state()
	let api: unknown = $state(null)
	let error: string | null = $state(null)
	let loading = $state(false)

	onMount(() => {
		if (!sheetmusicUrl || !containerEl) return

		let destroyed = false

		async function initAlphaTab() {
			try {
				loading = true
				const alphaTabModule = await import('@coderline/alphatab')
				if (destroyed) return

				const { AlphaTabApi, Settings, PlayerMode, NotationElement } = alphaTabModule

				const settings = new Settings()
				// @coderline/alphatab-vite 플러그인이 Bravura 폰트/사운드폰트를
				// <root>/font/ 와 <root>/soundfont/ 로 서빙한다 (/alphatab/* 아님).
				settings.core.fontDirectory = '/font/'
				settings.player.enablePlayer = true
				settings.player.playerMode = PlayerMode.EnabledExternalMedia
				settings.player.soundFont = '/soundfont/sonivox.sf2'

				// 오선지(악보)만 표시 — 제목/아티스트/트랙명 등 메타데이터 헤더 숨김
				const hiddenElements = [
					NotationElement.ScoreTitle,
					NotationElement.ScoreSubTitle,
					NotationElement.ScoreArtist,
					NotationElement.ScoreAlbum,
					NotationElement.ScoreWords,
					NotationElement.ScoreMusic,
					NotationElement.ScoreWordsAndMusic,
					NotationElement.ScoreCopyright,
					NotationElement.GuitarTuning,
					NotationElement.TrackNames
				]
				for (const el of hiddenElements) {
					settings.notation.elements.set(el, false)
				}

				const instance = new AlphaTabApi(containerEl!, settings)
				instance.load(sheetmusicUrl!)
				api = instance
			} catch (e) {
				if (!destroyed) {
					error = e instanceof Error ? e.message : '악보를 불러올 수 없습니다'
				}
			} finally {
				if (!destroyed) loading = false
			}
		}

		initAlphaTab()

		return () => {
			destroyed = true
			if (api && typeof (api as { destroy?: () => void }).destroy === 'function') {
				;(api as { destroy: () => void }).destroy()
			}
		}
	})
</script>

{#if !sheetmusicUrl}
	<div
		data-testid="tab-sheet-placeholder"
		class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] w-full"
		style="min-height: 200px;"
	>
		<div class="text-center">
			<div
				class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center"
			>
				<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
					<path
						d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"
					/>
				</svg>
			</div>
			<p class="text-[#666] text-sm">Tab Sheet</p>
		</div>
	</div>
{:else if error}
	<div
		data-testid="tab-sheet-error"
		class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] w-full"
		style="min-height: 200px;"
	>
		<div class="text-center">
			<p class="text-red-400 text-sm">{error}</p>
		</div>
	</div>
{:else}
	<div
		data-testid="tab-sheet"
		bind:this={containerEl}
		class="bg-[#fbfaf6] rounded-lg border border-[#2a2a2a] w-full overflow-auto p-4"
		style="min-height: 200px;"
	></div>
{/if}
