import { describe, it, expect } from 'vitest'
import {
	getLectureStatusMode,
	getSessionState,
	getLessonLastPosition,
	type LectureProgress
} from '$lib/features/lecture/utils/progress'

const progress = (overrides: Partial<LectureProgress> = {}): LectureProgress => ({
	completed_count: 0,
	total_count: 3,
	percent: 0,
	next_lesson_id: 700,
	completed_lesson_ids: [],
	lessons: [],
	resume_lesson_id: null,
	resume_position_sec: 0,
	...overrides
})

describe('getLectureStatusMode', () => {
	it('progress가 없으면 anonymous', () => {
		expect(getLectureStatusMode(null, false)).toBe('anonymous')
		expect(getLectureStatusMode(undefined, false)).toBe('anonymous')
	})

	it('인증됐지만 진도가 없으면(progress null) anonymous가 아닌 not-started로 본다', () => {
		expect(getLectureStatusMode(null, true)).toBe('anonymous')
	})

	it('progress 있고 completed=0 이면 not-started', () => {
		expect(getLectureStatusMode(progress({ completed_count: 0 }), true)).toBe('not-started')
	})

	it('progress 있고 completed>0 이면 in-progress', () => {
		expect(getLectureStatusMode(progress({ completed_count: 1, percent: 33 }), true)).toBe(
			'in-progress'
		)
	})

	it('accessible=true 이고 completed=0 이면 in-progress (0% 활성)', () => {
		expect(getLectureStatusMode(progress({ completed_count: 0 }), true, true)).toBe(
			'in-progress'
		)
	})

	it('accessible=false 이면 completed>0 이어도 not-started (티켓 미사용 우선)', () => {
		expect(
			getLectureStatusMode(progress({ completed_count: 2, percent: 66 }), true, false)
		).toBe('not-started')
	})

	it('accessible=true 이고 completed>0 이면 in-progress', () => {
		expect(
			getLectureStatusMode(progress({ completed_count: 1, percent: 33 }), true, true)
		).toBe('in-progress')
	})

	it('accessible 생략 시 기존 휴리스틱 유지', () => {
		expect(getLectureStatusMode(progress({ completed_count: 0 }), true)).toBe('not-started')
		expect(getLectureStatusMode(progress({ completed_count: 1 }), true)).toBe('in-progress')
	})

	it('비인증이면 accessible 값과 무관하게 anonymous', () => {
		expect(getLectureStatusMode(progress({ completed_count: 1 }), false, true)).toBe(
			'anonymous'
		)
		expect(getLectureStatusMode(progress({ completed_count: 1 }), false, false)).toBe(
			'anonymous'
		)
	})
})

describe('getSessionState', () => {
	it('완료된 세션은 completed', () => {
		const p = progress({ completed_lesson_ids: [700], next_lesson_id: 701 })
		expect(getSessionState(700, p, true)).toBe('completed')
	})

	it('next_lesson_id와 같으면 current', () => {
		const p = progress({ completed_lesson_ids: [700], next_lesson_id: 701 })
		expect(getSessionState(701, p, true)).toBe('current')
	})

	it('완료도 current도 아니면 upcoming', () => {
		const p = progress({ completed_lesson_ids: [700], next_lesson_id: 701 })
		expect(getSessionState(702, p, true)).toBe('upcoming')
	})

	it('비로그인이면 locked', () => {
		expect(getSessionState(700, null, false)).toBe('locked')
	})
})

describe('getLessonLastPosition', () => {
	it('lessons[]에서 lesson_id 매칭 last_position_sec를 반환', () => {
		const p = progress({
			lessons: [{ lesson_id: 700, percent: 42, completed: false, last_position_sec: 30 }]
		})
		expect(getLessonLastPosition(700, p)).toBe(30)
	})

	it('매칭 없으면 0', () => {
		expect(getLessonLastPosition(999, progress())).toBe(0)
		expect(getLessonLastPosition(700, null)).toBe(0)
	})
})
