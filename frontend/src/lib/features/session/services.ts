import { fetchSessionDetail } from '$lib/api/session'
import { reportLessonPosition as apiReportLessonPosition } from '$lib/api/progress'
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
