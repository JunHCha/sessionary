import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('VideoPlayer', () => {
	describe('getDefaultProps', () => {
		it('기본 props를 반환한다', async () => {
			const { getDefaultProps } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const defaults = getDefaultProps()

			expect(defaults.autoplay).toBe(false)
			expect(defaults.poster).toBeUndefined()
		})
	})

	describe('shouldUseHlsJs', () => {
		it('HLS 소스이고 네이티브 HLS 미지원 시 true를 반환한다', async () => {
			const { shouldUseHlsJs } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const result = shouldUseHlsJs('https://example.com/video.m3u8', false, true)
			expect(result).toBe(true)
		})

		it('HLS 소스이고 네이티브 HLS 지원 시 false를 반환한다', async () => {
			const { shouldUseHlsJs } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const result = shouldUseHlsJs('https://example.com/video.m3u8', true, true)
			expect(result).toBe(false)
		})

		it('MP4 소스는 항상 false를 반환한다', async () => {
			const { shouldUseHlsJs } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const result = shouldUseHlsJs('https://example.com/video.mp4', false, true)
			expect(result).toBe(false)
		})

		it('hls.js 미지원 환경에서는 false를 반환한다', async () => {
			const { shouldUseHlsJs } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const result = shouldUseHlsJs('https://example.com/video.m3u8', false, false)
			expect(result).toBe(false)
		})
	})

	describe('getVideoSource', () => {
		it('HLS 소스에 네이티브 지원 시 src를 반환한다', async () => {
			const { getVideoSource } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const src = getVideoSource('https://example.com/video.m3u8', true)
			expect(src).toBe('https://example.com/video.m3u8')
		})

		it('MP4 소스는 항상 src를 반환한다', async () => {
			const { getVideoSource } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const src = getVideoSource('https://example.com/video.mp4', false)
			expect(src).toBe('https://example.com/video.mp4')
		})

		it('HLS 소스에 네이티브 미지원 시 빈 문자열을 반환한다', async () => {
			const { getVideoSource } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			const src = getVideoSource('https://example.com/video.m3u8', false)
			expect(src).toBe('')
		})
	})

	describe('shouldClearLoading', () => {
		it('canplay 이벤트 시 로딩을 해제한다', async () => {
			const { shouldClearLoading } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldClearLoading('canplay')).toBe(true)
		})

		it('loadedmetadata 이벤트 시에도 로딩을 해제한다 (iOS Safari 대응)', async () => {
			const { shouldClearLoading } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldClearLoading('loadedmetadata')).toBe(true)
		})
	})

	describe('shouldShowPlayOverlay', () => {
		it('재생 시작 전이고 에러가 없으면 재생 오버레이를 표시한다', async () => {
			const { shouldShowPlayOverlay } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldShowPlayOverlay(false, false)).toBe(true)
		})

		it('재생이 시작되면 재생 오버레이를 숨긴다', async () => {
			const { shouldShowPlayOverlay } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldShowPlayOverlay(true, false)).toBe(false)
		})

		it('에러가 있으면 재생 오버레이를 표시하지 않는다 (에러 오버레이 우선)', async () => {
			const { shouldShowPlayOverlay } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldShowPlayOverlay(false, true)).toBe(false)
		})

		it('재생도 시작됐고 에러도 있으면 표시하지 않는다', async () => {
			const { shouldShowPlayOverlay } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(shouldShowPlayOverlay(true, true)).toBe(false)
		})
	})

	describe('SPINNER_OVERLAY_CLASS', () => {
		it('pointer-events-none을 포함해 아래 컨트롤 탭을 막지 않는다', async () => {
			const { SPINNER_OVERLAY_CLASS } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(SPINNER_OVERLAY_CLASS).toContain('pointer-events-none')
		})

		it('기존 오버레이 레이아웃 클래스를 유지한다', async () => {
			const { SPINNER_OVERLAY_CLASS } = await import(
				'$lib/features/session/components/VideoPlayer.svelte'
			)
			expect(SPINNER_OVERLAY_CLASS).toContain('absolute inset-0')
			expect(SPINNER_OVERLAY_CLASS).toContain('z-10')
		})
	})
})
