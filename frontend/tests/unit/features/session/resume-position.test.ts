import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('$lib/api/client/services.gen', () => ({
	getLectureLectureLectureIdGet: vi.fn()
}))

const lectureDetail = (progress: unknown) => ({
	data: {
		id: 10,
		title: 'L',
		artist: null,
		lessons: [],
		description: '',
		thumbnail: null,
		tags: null,
		length_sec: 0,
		lecture_count: 0,
		time_created: '',
		time_updated: '',
		progress
	}
})

describe('fetchLessonResumePosition', () => {
	beforeEach(() => {
		vi.clearAllMocks()
	})

	it('lecture progress.lessons에서 lesson_id 매칭 last_position_sec를 반환', async () => {
		const { getLectureLectureLectureIdGet } = await import('$lib/api/client/services.gen')
		const { fetchLessonResumePosition } = await import('$lib/features/session/services')

		vi.mocked(getLectureLectureLectureIdGet).mockResolvedValue(
			lectureDetail({
				completed_count: 0,
				total_count: 1,
				percent: 0,
				next_lesson_id: 700,
				completed_lesson_ids: [],
				lessons: [{ lesson_id: 700, percent: 40, completed: false, last_position_sec: 72 }],
				resume_lesson_id: 700,
				resume_position_sec: 72
			}) as any
		)

		const pos = await fetchLessonResumePosition(10, 700)
		expect(getLectureLectureLectureIdGet).toHaveBeenCalledWith({ lectureId: 10 })
		expect(pos).toBe(72)
	})

	it('매칭 레슨이 없으면 0', async () => {
		const { getLectureLectureLectureIdGet } = await import('$lib/api/client/services.gen')
		const { fetchLessonResumePosition } = await import('$lib/features/session/services')

		vi.mocked(getLectureLectureLectureIdGet).mockResolvedValue(
			lectureDetail({
				completed_count: 0,
				total_count: 1,
				percent: 0,
				next_lesson_id: 700,
				completed_lesson_ids: [],
				lessons: [],
				resume_lesson_id: null,
				resume_position_sec: 0
			}) as any
		)

		expect(await fetchLessonResumePosition(10, 700)).toBe(0)
	})

	it('progress가 null이면 0', async () => {
		const { getLectureLectureLectureIdGet } = await import('$lib/api/client/services.gen')
		const { fetchLessonResumePosition } = await import('$lib/features/session/services')

		vi.mocked(getLectureLectureLectureIdGet).mockResolvedValue(lectureDetail(null) as any)
		expect(await fetchLessonResumePosition(10, 700)).toBe(0)
	})

	it('에러 시 0을 반환하고 throw하지 않는다', async () => {
		const { getLectureLectureLectureIdGet } = await import('$lib/api/client/services.gen')
		const { fetchLessonResumePosition } = await import('$lib/features/session/services')

		vi.mocked(getLectureLectureLectureIdGet).mockRejectedValue(new Error('boom'))
		expect(await fetchLessonResumePosition(10, 700)).toBe(0)
	})
})
