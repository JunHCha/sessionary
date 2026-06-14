import type { LessonAdminDetail } from '$lib/api'

let draft = $state<LessonAdminDetail | null>(null)

export function setLessonDraft(lesson: LessonAdminDetail) {
	draft = lesson
}

export function takeLessonDraft(lessonId: number): LessonAdminDetail | null {
	if (draft && draft.id === lessonId) {
		return draft
	}
	return null
}
