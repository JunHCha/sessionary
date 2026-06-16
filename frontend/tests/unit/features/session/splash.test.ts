import { describe, it, expect } from 'vitest'

describe('splash 전환 게이트 로직', () => {
	describe('상수', () => {
		it('MIN_SPLASH_MS는 2000이다', async () => {
			const { MIN_SPLASH_MS } = await import('$lib/features/session/splash')
			expect(MIN_SPLASH_MS).toBe(2000)
		})

		it('PRELOAD_TIMEOUT_MS는 8000이다', async () => {
			const { PRELOAD_TIMEOUT_MS } = await import('$lib/features/session/splash')
			expect(PRELOAD_TIMEOUT_MS).toBe(8000)
		})
	})

	describe('shouldTransitionFromSplash', () => {
		it('2초 경과 + 리소스 준비 완료 시 true (approval)', async () => {
			const { shouldTransitionFromSplash } = await import('$lib/features/session/splash')
			expect(shouldTransitionFromSplash({ minElapsed: true, resourcesReady: true })).toBe(
				true
			)
		})

		it('2초 경과 전이면 false', async () => {
			const { shouldTransitionFromSplash } = await import('$lib/features/session/splash')
			expect(shouldTransitionFromSplash({ minElapsed: false, resourcesReady: true })).toBe(
				false
			)
		})

		it('리소스 미준비면 false', async () => {
			const { shouldTransitionFromSplash } = await import('$lib/features/session/splash')
			expect(shouldTransitionFromSplash({ minElapsed: true, resourcesReady: false })).toBe(
				false
			)
		})

		it('둘 다 미충족이면 false', async () => {
			const { shouldTransitionFromSplash } = await import('$lib/features/session/splash')
			expect(shouldTransitionFromSplash({ minElapsed: false, resourcesReady: false })).toBe(
				false
			)
		})
	})

	describe('areResourcesReady', () => {
		it('영상/자막/악보 모두 준비되면 true (approval)', async () => {
			const { areResourcesReady } = await import('$lib/features/session/splash')
			expect(areResourcesReady({ video: true, subtitles: true, sheet: true })).toBe(true)
		})

		it('영상 미준비면 false', async () => {
			const { areResourcesReady } = await import('$lib/features/session/splash')
			expect(areResourcesReady({ video: false, subtitles: true, sheet: true })).toBe(false)
		})

		it('자막 미준비면 false', async () => {
			const { areResourcesReady } = await import('$lib/features/session/splash')
			expect(areResourcesReady({ video: true, subtitles: false, sheet: true })).toBe(false)
		})

		it('악보 미준비면 false', async () => {
			const { areResourcesReady } = await import('$lib/features/session/splash')
			expect(areResourcesReady({ video: true, subtitles: true, sheet: false })).toBe(false)
		})
	})

	describe('isSheetReady', () => {
		it('악보 URL이 null이면 즉시 ready (true)', async () => {
			const { isSheetReady } = await import('$lib/features/session/splash')
			expect(isSheetReady(null, false)).toBe(true)
		})

		it('악보 URL이 있고 로드 완료면 ready', async () => {
			const { isSheetReady } = await import('$lib/features/session/splash')
			expect(isSheetReady('https://example.com/sheet.pdf', true)).toBe(true)
		})

		it('악보 URL이 있는데 미로드면 not ready', async () => {
			const { isSheetReady } = await import('$lib/features/session/splash')
			expect(isSheetReady('https://example.com/sheet.pdf', false)).toBe(false)
		})
	})

	describe('isVideoReady', () => {
		it('영상 URL이 빈 문자열이면 즉시 ready (영상 없는 세션)', async () => {
			const { isVideoReady } = await import('$lib/features/session/splash')
			expect(isVideoReady('', false)).toBe(true)
		})

		it('영상 URL이 있고 프리로드 완료면 ready', async () => {
			const { isVideoReady } = await import('$lib/features/session/splash')
			expect(isVideoReady('https://example.com/v.m3u8', true)).toBe(true)
		})

		it('영상 URL이 있는데 미프리로드면 not ready', async () => {
			const { isVideoReady } = await import('$lib/features/session/splash')
			expect(isVideoReady('https://example.com/v.mp4', false)).toBe(false)
		})
	})

	describe('videoPreloadEventToReady', () => {
		it('MP4 loadedmetadata는 ready 신호로 본다', async () => {
			const { videoPreloadEventToReady } = await import('$lib/features/session/splash')
			expect(videoPreloadEventToReady('loadedmetadata')).toBe(true)
		})

		it('HLS manifestparsed는 ready 신호로 본다', async () => {
			const { videoPreloadEventToReady } = await import('$lib/features/session/splash')
			expect(videoPreloadEventToReady('manifestparsed')).toBe(true)
		})

		it('canplay는 ready 신호로 본다', async () => {
			const { videoPreloadEventToReady } = await import('$lib/features/session/splash')
			expect(videoPreloadEventToReady('canplay')).toBe(true)
		})

		it('알 수 없는 이벤트는 ready 아님', async () => {
			const { videoPreloadEventToReady } = await import('$lib/features/session/splash')
			expect(videoPreloadEventToReady('progress')).toBe(false)
		})
	})
})
