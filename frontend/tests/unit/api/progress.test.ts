import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('$lib/api/client/services.gen', () => ({
	reportLessonPositionProgressLessonLessonIdPositionPut: vi.fn()
}))

describe('Progress API Service', () => {
	beforeEach(() => {
		vi.clearAllMocks()
	})

	describe('reportLessonPosition', () => {
		it('lessonId/position/duration으로 PUT position을 호출한다', async () => {
			const { reportLessonPositionProgressLessonLessonIdPositionPut } = await import(
				'$lib/api/client/services.gen'
			)
			const { reportLessonPosition } = await import('$lib/api/progress')

			const mockResponse = { percent: 50 }
			vi.mocked(reportLessonPositionProgressLessonLessonIdPositionPut).mockResolvedValue(
				mockResponse as any
			)

			const result = await reportLessonPosition(700, 45, 90)

			expect(reportLessonPositionProgressLessonLessonIdPositionPut).toHaveBeenCalledWith({
				lessonId: 700,
				requestBody: { position_sec: 45, duration_sec: 90 }
			})
			expect(result).toEqual(mockResponse)
		})

		it('position/duration을 정수로 반올림하여 전송한다', async () => {
			const { reportLessonPositionProgressLessonLessonIdPositionPut } = await import(
				'$lib/api/client/services.gen'
			)
			const { reportLessonPosition } = await import('$lib/api/progress')

			vi.mocked(reportLessonPositionProgressLessonLessonIdPositionPut).mockResolvedValue({} as any)

			await reportLessonPosition(700, 45.7, 90.2)

			expect(reportLessonPositionProgressLessonLessonIdPositionPut).toHaveBeenCalledWith({
				lessonId: 700,
				requestBody: { position_sec: 46, duration_sec: 90 }
			})
		})
	})
})
