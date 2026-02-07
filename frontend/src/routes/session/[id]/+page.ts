import type { PageLoad } from './$types'
import { parseSessionId } from '$lib/features/session/utils'

export const load: PageLoad = async ({ params }) => {
	const sessionId = parseSessionId(params.id)
	return { sessionId }
}
