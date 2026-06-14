import type { PageLoad } from './$types'

export const load: PageLoad = async ({ params }) => {
	return { lectureId: Number(params.id) }
}
