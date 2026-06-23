import type { LectureProgressData } from '$lib/api/client'

export type LectureProgress = LectureProgressData

export type LectureStatusMode = 'anonymous' | 'not-started' | 'in-progress'

export type SessionState = 'completed' | 'current' | 'upcoming' | 'locked'

export function getLectureStatusMode(
	progress: LectureProgress | null | undefined,
	isAuthenticated: boolean,
	accessible?: boolean | null
): LectureStatusMode {
	if (!progress || !isAuthenticated) {
		return 'anonymous'
	}
	if (accessible === true) {
		return 'in-progress'
	}
	if (accessible === false) {
		return 'not-started'
	}
	return progress.completed_count > 0 ? 'in-progress' : 'not-started'
}

export function getSessionState(
	lessonId: number,
	progress: LectureProgress | null | undefined,
	isAuthenticated: boolean
): SessionState {
	if (!progress || !isAuthenticated) {
		return 'locked'
	}
	if (progress.completed_lesson_ids.includes(lessonId)) {
		return 'completed'
	}
	if (progress.next_lesson_id === lessonId) {
		return 'current'
	}
	return 'upcoming'
}
