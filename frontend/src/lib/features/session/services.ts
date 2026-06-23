import { fetchSessionDetail } from '$lib/api/session'
import { reportLessonPosition as apiReportLessonPosition } from '$lib/api/progress'
import { getLectureLectureLectureIdGet } from '$lib/api/client/services.gen'
import { toSessionDetailData, type SessionDetailData } from './types'

export async function loadSessionDetail(sessionId: number): Promise<SessionDetailData> {
	const response = await fetchSessionDetail(sessionId)
	return toSessionDetailData(response)
}

/**
 * 시청 위치 리포팅 (fire-and-forget). 에러는 콘솔에만 남기고 throw 하지 않는다.
 * @returns 갱신된 LectureProgressData (실패 시 null)
 */
export async function reportLessonPosition(
	lessonId: number,
	positionSec: number,
	durationSec: number
) {
	try {
		return await apiReportLessonPosition(lessonId, positionSec, durationSec)
	} catch (e) {
		console.error('[session] 위치 리포팅 실패', e)
		return null
	}
}

/**
 * 이어보기 위치 조회. 렉처 진행도의 lessons[]에서 해당 lesson_id의
 * last_position_sec 를 추출한다. 실패/미존재 시 0(처음부터).
 */
export async function fetchLessonResumePosition(
	lectureId: number,
	lessonId: number
): Promise<number> {
	try {
		const res = await getLectureLectureLectureIdGet({ lectureId })
		const item = res.data.progress?.lessons?.find((l) => l.lesson_id === lessonId)
		return item?.last_position_sec ?? 0
	} catch (e) {
		console.error('[session] 이어보기 위치 조회 실패', e)
		return 0
	}
}
