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

				const { AlphaTabApi, Settings, PlayerMode, NotationElement, LayoutMode } =
					alphaTabModule

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

				// 한 줄 가로 레이아웃 + 컴팩트 스케일 → 고정 높이 + 가로 스크롤만
				settings.display.layoutMode = LayoutMode.Horizontal
				settings.display.scale = 0.9

				const instance = new AlphaTabApi(containerEl!, settings)
				// 비동기 로드/렌더 에러도 표면화 (try/catch 는 동기 에러만 잡음)
				instance.error.on((e: unknown) => {
					if (!destroyed) {
						error = e instanceof Error ? e.message : '악보를 렌더링할 수 없습니다'
					}
				})
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
		class="tab-sheet-card flex items-center w-full overflow-x-auto overflow-y-hidden rounded-xl border border-[#2b2b2b]"
	>
		<div bind:this={containerEl} class="w-full"></div>
	</div>
{/if}

<style>
	/* 어두운 UI 위에 떠 있는 '종이' 카드 — 따뜻한 크림 그라데이션 + 깊이감 */
	.tab-sheet-card {
		height: 232px;
		padding: 16px 20px;
		background:
			radial-gradient(120% 80% at 50% 0%, #ffffff 0%, #f6f1e4 55%, #eae1cd 100%);
		box-shadow:
			0 16px 40px rgba(0, 0, 0, 0.5),
			0 2px 6px rgba(0, 0, 0, 0.35),
			inset 0 1px 0 rgba(255, 255, 255, 0.85);
	}
</style>
