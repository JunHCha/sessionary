import { describe, it, expect } from 'vitest'
import type { SessionDetailResponse } from '$lib/api/client/types.gen'

function createMockSessionDetailResponse(): SessionDetailResponse {
	return {
		id: 42,
		title: '기본 코드 잡기',
		session_type: 'PLAY' as const,
		session_type_label: '연주',
		lecture_ordering: 3,
		length_sec: 180,
		lecture: {
			id: 10,
			title: '기타 입문 강좌',
			total_sessions: 8
		},
		video: {
			url: 'https://cdn.example.com/video.m3u8',
			type: 'hls',
			expires_at: '2025-12-31T23:59:59Z'
		},
		sheetmusic_url: 'https://cdn.example.com/sheet.pdf',
		sync_offset: 500,
		subtitles: [
			{ timestamp_ms: 0, text: '안녕하세요' },
			{ timestamp_ms: 3000, text: '오늘은 기본 코드를 배워보겠습니다' }
		],
		playing_guide: [
			{
				step: 1,
				title: '손가락 위치',
				description: '검지를 2번 줄 1프렛에 놓으세요',
				start_time: '00:00',
				end_time: '00:30',
				tip: '힘을 빼세요'
			}
		],
		navigation: {
			prev_session_id: 41,
			next_session_id: 43
		}
	}
}

describe('Session Detail Types', () => {
	describe('toSessionDetailData', () => {
		it('API 응답의 기본 필드를 올바르게 매핑한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.id).toBe(42)
			expect(data.title).toBe('기본 코드 잡기')
			expect(data.sessionType).toBe('PLAY')
			expect(data.sessionTypeLabel).toBe('연주')
			expect(data.lectureOrdering).toBe(3)
			expect(data.lengthSec).toBe(180)
			expect(data.syncOffset).toBe(500)
		})

		it('lecture 정보를 평탄화하여 매핑한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.lectureId).toBe(10)
			expect(data.lectureTitle).toBe('기타 입문 강좌')
			expect(data.totalSessions).toBe(8)
		})

		it('video가 있으면 videoUrl과 videoType을 추출한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.videoUrl).toBe('https://cdn.example.com/video.m3u8')
			expect(data.videoType).toBe('hls')
		})

		it('video가 null이면 videoUrl은 빈 문자열, videoType은 빈 문자열이다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			response.video = null
			const data = toSessionDetailData(response)

			expect(data.videoUrl).toBe('')
			expect(data.videoType).toBe('')
		})

		it('navigation에서 prev/next session id를 추출한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.prevSessionId).toBe(41)
			expect(data.nextSessionId).toBe(43)
		})

		it('navigation의 prev/next가 null이면 null을 유지한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			response.navigation = { prev_session_id: null, next_session_id: null }
			const data = toSessionDetailData(response)

			expect(data.prevSessionId).toBeNull()
			expect(data.nextSessionId).toBeNull()
		})

		it('subtitles와 playing_guide를 그대로 전달한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.subtitles).toEqual([
				{ timestamp_ms: 0, text: '안녕하세요' },
				{ timestamp_ms: 3000, text: '오늘은 기본 코드를 배워보겠습니다' }
			])
			expect(data.playingGuide).toEqual([
				{
					step: 1,
					title: '손가락 위치',
					description: '검지를 2번 줄 1프렛에 놓으세요',
					start_time: '00:00',
					end_time: '00:30',
					tip: '힘을 빼세요'
				}
			])
		})

		it('sheetmusicUrl을 매핑한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			const data = toSessionDetailData(response)

			expect(data.sheetmusicUrl).toBe('https://cdn.example.com/sheet.pdf')
		})

		it('sheetmusic_url이 null이면 null을 유지한다', async () => {
			const { toSessionDetailData } = await import('$lib/features/session/types')
			const response = createMockSessionDetailResponse()
			response.sheetmusic_url = null
			const data = toSessionDetailData(response)

			expect(data.sheetmusicUrl).toBeNull()
		})
	})
})
