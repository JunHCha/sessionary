import { describe, it, expect } from 'vitest'

describe('Video Utils', () => {
	describe('formatTime', () => {
		it('0초를 "0:00"으로 포맷한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(0)).toBe('0:00')
		})

		it('59초를 "0:59"로 포맷한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(59)).toBe('0:59')
		})

		it('60초를 "1:00"으로 포맷한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(60)).toBe('1:00')
		})

		it('125초를 "2:05"로 포맷한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(125)).toBe('2:05')
		})

		it('3661초를 "61:01"로 포맷한다 (1시간 이상)', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(3661)).toBe('61:01')
		})

		it('NaN은 "0:00"으로 처리한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(NaN)).toBe('0:00')
		})

		it('음수는 "0:00"으로 처리한다', async () => {
			const { formatTime } = await import('$lib/features/session/utils')
			expect(formatTime(-10)).toBe('0:00')
		})
	})

	describe('isHlsSource', () => {
		it('.m3u8 확장자를 HLS로 인식한다', async () => {
			const { isHlsSource } = await import('$lib/features/session/utils')
			expect(isHlsSource('https://example.com/video.m3u8')).toBe(true)
		})

		it('.M3U8 대문자도 HLS로 인식한다', async () => {
			const { isHlsSource } = await import('$lib/features/session/utils')
			expect(isHlsSource('https://example.com/video.M3U8')).toBe(true)
		})

		it('.mp4 확장자는 HLS가 아니다', async () => {
			const { isHlsSource } = await import('$lib/features/session/utils')
			expect(isHlsSource('https://example.com/video.mp4')).toBe(false)
		})

		it('쿼리 파라미터가 있어도 .m3u8을 인식한다', async () => {
			const { isHlsSource } = await import('$lib/features/session/utils')
			expect(isHlsSource('https://example.com/video.m3u8?token=abc')).toBe(true)
		})
	})

	describe('PLAYBACK_SPEEDS', () => {
		it('5개의 재생 속도 옵션이 있다', async () => {
			const { PLAYBACK_SPEEDS } = await import('$lib/features/session/utils')
			expect(PLAYBACK_SPEEDS).toHaveLength(5)
		})

		it('기본 속도 1.0이 포함되어 있다', async () => {
			const { PLAYBACK_SPEEDS } = await import('$lib/features/session/utils')
			expect(PLAYBACK_SPEEDS).toContain(1.0)
		})

		it('속도가 오름차순으로 정렬되어 있다', async () => {
			const { PLAYBACK_SPEEDS } = await import('$lib/features/session/utils')
			const sorted = [...PLAYBACK_SPEEDS].sort((a, b) => a - b)
			expect(PLAYBACK_SPEEDS).toEqual(sorted)
		})
	})
})
