import { redirect, type Handle, type HandleServerError } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
	try {
		const response = await resolve(event)
		return response
	} catch (e) {
		if (e instanceof Error) {
			// 404 에러일 경우 not-found로 리다이렉트
			if (e.message.includes('Not found')) {
				throw redirect(303, '/not-found')
			}
		}
		throw e
	}
}

// 모든 에러를 처리하는 handleError 추가
export const handleError: HandleServerError = ({ error }) => {
	// 404 에러 처리
	if (error instanceof Error && error.message.includes('Not found')) {
		throw redirect(303, '/not-found')
	}
	return {
		message: 'Whoops!',
		code: error instanceof Error ? error.message : 'UNKNOWN'
	}
}
