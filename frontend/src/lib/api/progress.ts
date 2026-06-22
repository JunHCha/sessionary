import { reportLessonPositionProgressLessonLessonIdPositionPut } from './client/services.gen'
import type { LectureProgressData } from './client/types.gen'

export async function reportLessonPosition(
	lessonId: number,
	positionSec: number,
	durationSec: number
): Promise<LectureProgressData> {
	return await reportLessonPositionProgressLessonLessonIdPositionPut({
		lessonId,
		requestBody: {
			position_sec: Math.round(positionSec),
			duration_sec: Math.round(durationSec)
		}
	})
}
