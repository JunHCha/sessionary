import { fetchSessionDetail } from '$lib/api/session'
import { toSessionDetailData, type SessionDetailData } from './types'

export async function loadSessionDetail(sessionId: number): Promise<SessionDetailData> {
	const response = await fetchSessionDetail(sessionId)
	return toSessionDetailData(response)
}
