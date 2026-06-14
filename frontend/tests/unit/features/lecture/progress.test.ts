import { describe, it, expect } from 'vitest'
import {
	getLectureStatusMode,
	getSessionState,
	type LectureProgress
} from '$lib/features/lecture/utils/progress'

const progress = (overrides: Partial<LectureProgress> = {}): LectureProgress => ({
	completed_count: 0,
	total_count: 3,
	percent: 0,
	next_lesson_id: 700,
	completed_lesson_ids: [],
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
