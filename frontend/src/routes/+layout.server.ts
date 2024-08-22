import { env } from '$env/dynamic/public'
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = async () => {
	return {
		env: {
			PUBLIC_API_BASE_URL: env.PUBLIC_API_BASE_URL
		}
	}
}
