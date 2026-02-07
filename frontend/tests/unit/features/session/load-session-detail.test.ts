import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('$lib/api/session', () => ({
	fetchSessionDetail: vi.fn()
}))

function createMockApiResponse() {
	return {
		id: 42,
		title: '기본 코드 잡기',
		session_type: 'PLAY' as const,
		session_type_label: '연주',
		lecture_ordering: 3,
		length_sec: 180,
		lecture: { id: 10, title: '기타 입문 강좌', total_sessions: 8 },
		video: {
			url: 'https://cdn.example.com/video.m3u8',
			type: 'hls',
			expires_at: '2025-12-31T23:59:59Z'
		},
		sheetmusic_url: 'https://cdn.example.com/sheet.pdf',
		sync_offset: 500,
		subtitles: [{ timestamp_ms: 0, text: '안녕하세요' }],
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
		navigation: { prev_session_id: 41, next_session_id: 43 }
	}
}

describe('loadSessionDetail', () => {
	beforeEach(() => {
		vi.clearAllMocks()
	})

	it('API 응답을 SessionDetailData로 변환하여 반환한다', async () => {
		const { fetchSessionDetail } = await import('$lib/api/session')
		const { loadSessionDetail } = await import('$lib/features/session/services')

		const mockResponse = createMockApiResponse()
		vi.mocked(fetchSessionDetail).mockResolvedValue(mockResponse as any)

		const result = await loadSessionDetail(42)

		expect(fetchSessionDetail).toHaveBeenCalledWith(42)
		expect(result.id).toBe(42)
		expect(result.title).toBe('기본 코드 잡기')
		expect(result.sessionType).toBe('PLAY')
		expect(result.lectureId).toBe(10)
		expect(result.videoUrl).toBe('https://cdn.example.com/video.m3u8')
		expect(result.prevSessionId).toBe(41)
		expect(result.nextSessionId).toBe(43)
	})

	it('API 에러를 그대로 전파한다', async () => {
		const { fetchSessionDetail } = await import('$lib/api/session')
		const { loadSessionDetail } = await import('$lib/features/session/services')

		vi.mocked(fetchSessionDetail).mockRejectedValue(new Error('Session not found'))

		await expect(loadSessionDetail(999)).rejects.toThrow('Session not found')
	})

	it('video가 null인 응답도 올바르게 변환한다', async () => {
		const { fetchSessionDetail } = await import('$lib/api/session')
		const { loadSessionDetail } = await import('$lib/features/session/services')

		const mockResponse = createMockApiResponse()
		mockResponse.video = null as any
		vi.mocked(fetchSessionDetail).mockResolvedValue(mockResponse as any)

		const result = await loadSessionDetail(42)

		expect(result.videoUrl).toBe('')
		expect(result.videoType).toBe('')
	})
})
