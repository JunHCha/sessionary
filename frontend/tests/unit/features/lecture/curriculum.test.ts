import { describe, it, expect } from 'vitest'
import {
	formatTotalLength,
	getDifficultyLabel,
	buildMinimap,
	getResumeLessonId,
	getFirstLessonId,
	type MinimapCell
} from '$lib/features/lecture/utils/curriculum'
import type { LectureProgress } from '$lib/features/lecture/utils/progress'

const progress = (overrides: Partial<LectureProgress> = {}): LectureProgress => ({
	completed_count: 0,
	total_count: 3,
	percent: 0,
	next_lesson_id: 700,
	completed_lesson_ids: [],
	...overrides
})

const lessons = [
	{ id: 700, lecture_ordering: 1 },
	{ id: 701, lecture_ordering: 2 },
	{ id: 702, lecture_ordering: 3 }
]

describe('formatTotalLength', () => {
	it('초를 시간:분 형태로 변환한다', () => {
		expect(formatTotalLength(6480)).toBe('1:48')
	})

	it('1시간 미만은 0:MM 형태', () => {
		expect(formatTotalLength(2400)).toBe('0:40')
	})

	it('0초는 0:00', () => {
		expect(formatTotalLength(0)).toBe('0:00')
	})
})

describe('getDifficultyLabel', () => {
	it('Intermediate 태그면 중급', () => {
		expect(getDifficultyLabel(['Intermediate'])).toBe('중급')
	})

	it('Easy 태그면 초급', () => {
		expect(getDifficultyLabel(['Easy'])).toBe('초급')
	})

	it('Advanced 태그면 고급', () => {
		expect(getDifficultyLabel(['Advanced'])).toBe('고급')
	})

	it('난이도 태그가 없으면 대시', () => {
		expect(getDifficultyLabel(['해석버전'])).toBe('-')
		expect(getDifficultyLabel(null)).toBe('-')
	})
})

describe('buildMinimap', () => {
	it('순서대로 done/current/upcoming 셀을 만든다', () => {
		const p = progress({ completed_lesson_ids: [700], next_lesson_id: 701, completed_count: 1 })
		const cells: MinimapCell[] = buildMinimap(lessons, p, true)
		expect(cells).toEqual(['done', 'current', 'upcoming'])
	})

	it('비로그인이면 모두 locked', () => {
		const cells = buildMinimap(lessons, null, false)
		expect(cells).toEqual(['locked', 'locked', 'locked'])
	})

	it('미수강이면 1강이 current, 나머지 upcoming', () => {
		const p = progress({ next_lesson_id: 700, completed_count: 0 })
		const cells = buildMinimap(lessons, p, true)
		expect(cells).toEqual(['current', 'upcoming', 'upcoming'])
	})
})

describe('getResumeLessonId', () => {
	it('next_lesson_id를 우선 반환한다', () => {
		const p = progress({ next_lesson_id: 701 })
		expect(getResumeLessonId(lessons, p, true)).toBe(701)
	})

	it('next_lesson_id가 없으면 첫 세션', () => {
		const p = progress({ next_lesson_id: null })
		expect(getResumeLessonId(lessons, p, true)).toBe(700)
	})

	it('비로그인이면 첫 세션', () => {
		expect(getResumeLessonId(lessons, null, false)).toBe(700)
	})

	it('세션이 없으면 null', () => {
		expect(getResumeLessonId([], null, false)).toBeNull()
	})
})

describe('getFirstLessonId', () => {
	it('lecture_ordering 가장 낮은 세션 id', () => {
		const shuffled = [
			{ id: 702, lecture_ordering: 3 },
			{ id: 700, lecture_ordering: 1 },
			{ id: 701, lecture_ordering: 2 }
		]
		expect(getFirstLessonId(shuffled)).toBe(700)
	})

	it('세션이 없으면 null', () => {
		expect(getFirstLessonId([])).toBeNull()
	})
})
