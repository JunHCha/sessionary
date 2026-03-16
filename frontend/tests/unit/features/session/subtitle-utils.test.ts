import { describe, it, expect } from 'vitest'

describe('findActiveSubtitleIndex', () => {
	it('빈 배열이면 -1을 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		expect(findActiveSubtitleIndex([], 5000)).toBe(-1)
	})

	it('첫 자막 시간 이전이면 -1을 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		const subtitles = [
			{ timestamp_ms: 3000, text: '첫 자막' },
			{ timestamp_ms: 6000, text: '두번째 자막' }
		]
		expect(findActiveSubtitleIndex(subtitles, 1000)).toBe(-1)
	})

	it('현재 시간에 해당하는 자막 인덱스를 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		const subtitles = [
			{ timestamp_ms: 1000, text: '첫 자막' },
			{ timestamp_ms: 5000, text: '두번째 자막' },
			{ timestamp_ms: 10000, text: '세번째 자막' }
		]
		expect(findActiveSubtitleIndex(subtitles, 7000)).toBe(1)
	})

	it('정확히 자막 시간과 일치하면 해당 인덱스를 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		const subtitles = [
			{ timestamp_ms: 1000, text: '첫 자막' },
			{ timestamp_ms: 5000, text: '두번째 자막' }
		]
		expect(findActiveSubtitleIndex(subtitles, 5000)).toBe(1)
	})

	it('마지막 자막 이후 시간이면 마지막 인덱스를 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		const subtitles = [
			{ timestamp_ms: 1000, text: '첫 자막' },
			{ timestamp_ms: 5000, text: '두번째 자막' }
		]
		expect(findActiveSubtitleIndex(subtitles, 99000)).toBe(1)
	})

	it('두 자막 사이 시간이면 이전 자막 인덱스를 반환한다', async () => {
		const { findActiveSubtitleIndex } = await import('$lib/features/session/utils')
		const subtitles = [
			{ timestamp_ms: 1000, text: '첫 자막' },
			{ timestamp_ms: 5000, text: '두번째 자막' },
			{ timestamp_ms: 10000, text: '세번째 자막' }
		]
		expect(findActiveSubtitleIndex(subtitles, 4999)).toBe(0)
	})
})

describe('formatSubtitleTimestamp', () => {
	it('0ms를 "0:00"으로 변환한다', async () => {
		const { formatSubtitleTimestamp } = await import('$lib/features/session/utils')
		expect(formatSubtitleTimestamp(0)).toBe('0:00')
	})

	it('밀리초를 분:초 형식으로 변환한다', async () => {
		const { formatSubtitleTimestamp } = await import('$lib/features/session/utils')
		expect(formatSubtitleTimestamp(125000)).toBe('2:05')
	})

	it('60초 이상을 올바르게 변환한다', async () => {
		const { formatSubtitleTimestamp } = await import('$lib/features/session/utils')
		expect(formatSubtitleTimestamp(60000)).toBe('1:00')
	})

	it('소수점 밀리초는 버림한다', async () => {
		const { formatSubtitleTimestamp } = await import('$lib/features/session/utils')
		expect(formatSubtitleTimestamp(61500)).toBe('1:01')
	})
})
