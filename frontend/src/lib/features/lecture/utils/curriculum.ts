import type { LectureProgress, SessionState } from './progress'
import { getSessionState, getLessonPercent } from './progress'

export type MinimapCell = 'done' | 'current' | 'upcoming' | 'partial' | 'locked'

type OrderedLesson = {
	id: number
	lecture_ordering: number
}

export function formatTotalLength(seconds: number): string {
	const hours = Math.floor(seconds / 3600)
	const minutes = Math.floor((seconds % 3600) / 60)
	return `${hours}:${minutes.toString().padStart(2, '0')}`
}

const DIFFICULTY_LABELS: Record<string, string> = {
	Easy: '초급',
	Intermediate: '중급',
	Advanced: '고급'
}

export function getDifficultyLabel(tags: unknown[] | null | undefined): string {
	if (!tags) return '-'
	for (const tag of tags) {
		const label = DIFFICULTY_LABELS[String(tag)]
		if (label) return label
	}
	return '-'
}

const STATE_TO_CELL: Record<SessionState, MinimapCell> = {
	completed: 'done',
	current: 'current',
	upcoming: 'upcoming',
	locked: 'locked'
}

export function buildMinimap(
	lessons: OrderedLesson[],
	progress: LectureProgress | null | undefined,
	isAuthenticated: boolean
): MinimapCell[] {
	return sortByOrdering(lessons).map((lesson) => {
		const state = getSessionState(lesson.id, progress, isAuthenticated)
		if (state === 'upcoming' && getLessonPercent(lesson.id, progress) > 0) {
			return 'partial'
		}
		return STATE_TO_CELL[state]
	})
}

export function getFirstLessonId(lessons: OrderedLesson[]): number | null {
	const sorted = sortByOrdering(lessons)
	return sorted.length > 0 ? sorted[0].id : null
}

export function getResumeLessonId(
	lessons: OrderedLesson[],
	progress: LectureProgress | null | undefined,
	isAuthenticated: boolean
): number | null {
	if (isAuthenticated && progress?.resume_lesson_id != null) {
		return progress.resume_lesson_id
	}
	if (isAuthenticated && progress?.next_lesson_id != null) {
		return progress.next_lesson_id
	}
	return getFirstLessonId(lessons)
}

function sortByOrdering<T extends OrderedLesson>(lessons: T[]): T[] {
	return [...lessons].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
}
