import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('$lib/api/client/services.gen', () => ({
	getSessionDetailSessionSessionIdGet: vi.fn()
}))

describe('Session API Service', () => {
	beforeEach(() => {
		vi.clearAllMocks()
	})

	describe('fetchSessionDetail', () => {
		it('sessionId로 API를 호출하고 응답을 반환한다', async () => {
			const { getSessionDetailSessionSessionIdGet } = await import(
				'$lib/api/client/services.gen'
			)
			const { fetchSessionDetail } = await import('$lib/api/session')

			const mockResponse = {
				id: 1,
				title: 'Test Session',
				session_type: 'PLAY' as const,
				session_type_label: '연주',
				lecture_ordering: 1,
				length_sec: 120,
				lecture: { id: 10, title: 'Test Lecture', total_sessions: 5 },
				video: { url: 'https://example.com/video.m3u8', type: 'hls', expires_at: '2025-12-31' },
				sheetmusic_url: null,
				sync_offset: 0,
				subtitles: [],
				playing_guide: [],
				navigation: { prev_session_id: null, next_session_id: 2 }
			}
			vi.mocked(getSessionDetailSessionSessionIdGet).mockResolvedValue(mockResponse as any)

			const result = await fetchSessionDetail(1)

			expect(getSessionDetailSessionSessionIdGet).toHaveBeenCalledWith({ sessionId: 1 })
			expect(result).toEqual(mockResponse)
		})

		it('API 에러를 그대로 throw한다', async () => {
			const { getSessionDetailSessionSessionIdGet } = await import(
				'$lib/api/client/services.gen'
			)
			const { fetchSessionDetail } = await import('$lib/api/session')

			const apiError = new Error('Session not found')
			vi.mocked(getSessionDetailSessionSessionIdGet).mockRejectedValue(apiError)

			await expect(fetchSessionDetail(999)).rejects.toThrow('Session not found')
		})
	})
})
