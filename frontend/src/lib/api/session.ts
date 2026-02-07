import { getSessionDetailSessionSessionIdGet } from './client/services.gen'
import type { SessionDetailResponse } from './client/types.gen'

export async function fetchSessionDetail(sessionId: number): Promise<SessionDetailResponse> {
	return await getSessionDetailSessionSessionIdGet({ sessionId })
}
