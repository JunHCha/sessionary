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
})
