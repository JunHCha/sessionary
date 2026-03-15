import { describe, it, expect } from 'vitest'

describe('TabSheet', () => {
	describe('createExternalMediaHandler', () => {
		it('backingTrackDuration을 밀리초로 반환한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			const handler = createExternalMediaHandler({
				videoDuration: 120,
				videoPlaybackRate: 1,
				videoVolume: 0.8,
				onSeek: () => {},
				onPlay: () => {},
				onPause: () => {}
			})

			expect(handler.backingTrackDuration).toBe(120000)
		})

		it('playbackRate를 반환한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			const handler = createExternalMediaHandler({
				videoDuration: 100,
				videoPlaybackRate: 1.5,
				videoVolume: 1,
				onSeek: () => {},
				onPlay: () => {},
				onPause: () => {}
			})

			expect(handler.playbackRate).toBe(1.5)
		})

		it('masterVolume를 반환한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			const handler = createExternalMediaHandler({
				videoDuration: 100,
				videoPlaybackRate: 1,
				videoVolume: 0.5,
				onSeek: () => {},
				onPlay: () => {},
				onPause: () => {}
			})

			expect(handler.masterVolume).toBe(0.5)
		})

		it('seekTo가 밀리초를 초로 변환하여 onSeek을 호출한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			let seekedTo = -1
			const handler = createExternalMediaHandler({
				videoDuration: 100,
				videoPlaybackRate: 1,
				videoVolume: 1,
				onSeek: (time) => {
					seekedTo = time
				},
				onPlay: () => {},
				onPause: () => {}
			})

			handler.seekTo(5000)
			expect(seekedTo).toBe(5)
		})

		it('play가 onPlay 콜백을 호출한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			let played = false
			const handler = createExternalMediaHandler({
				videoDuration: 100,
				videoPlaybackRate: 1,
				videoVolume: 1,
				onSeek: () => {},
				onPlay: () => {
					played = true
				},
				onPause: () => {}
			})

			handler.play()
			expect(played).toBe(true)
		})

		it('pause가 onPause 콜백을 호출한다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			let paused = false
			const handler = createExternalMediaHandler({
				videoDuration: 100,
				videoPlaybackRate: 1,
				videoVolume: 1,
				onSeek: () => {},
				onPlay: () => {},
				onPause: () => {
					paused = true
				}
			})

			handler.pause()
			expect(paused).toBe(true)
		})

		it('videoDuration이 0일 때 backingTrackDuration은 0이다', async () => {
			const { createExternalMediaHandler } =
				await import('$lib/features/session/components/TabSheet.svelte')
			const handler = createExternalMediaHandler({
				videoDuration: 0,
				videoPlaybackRate: 1,
				videoVolume: 1,
				onSeek: () => {},
				onPlay: () => {},
				onPause: () => {}
			})

			expect(handler.backingTrackDuration).toBe(0)
		})
	})
})
