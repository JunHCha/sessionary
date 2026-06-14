import { describe, it, expect } from 'vitest'
import { parseSubtitles } from '$lib/features/admin/utils/subtitle-parser'

describe('parseSubtitles', () => {
	it('SRT를 timestamp_ms/text 배열로 변환', () => {
		const srt = `1\n00:00:00,000 --> 00:00:02,000\n안녕하세요\n\n2\n00:00:02,500 --> 00:00:04,000\n반갑습니다`
		expect(parseSubtitles(srt)).toEqual([
			{ timestamp_ms: 0, text: '안녕하세요' },
			{ timestamp_ms: 2500, text: '반갑습니다' }
		])
	})

	it('WEBVTT 헤더와 점(.) 밀리초 처리', () => {
		const vtt = `WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nhello`
		expect(parseSubtitles(vtt)).toEqual([{ timestamp_ms: 1000, text: 'hello' }])
	})

	it('여러 줄 텍스트는 공백으로 합침', () => {
		const srt = `1\n00:00:00,000 --> 00:00:01,000\na\nb`
		expect(parseSubtitles(srt)).toEqual([{ timestamp_ms: 0, text: 'a b' }])
	})

	it('빈 입력은 빈 배열', () => {
		expect(parseSubtitles('')).toEqual([])
	})
})
