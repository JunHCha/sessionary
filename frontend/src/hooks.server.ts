import { redirect, type Handle, type HandleServerError } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
	try {
		const response = await resolve(event)
		return response
	} catch (e) {
		if (e instanceof Error) {
			if (e.message.includes('Not found')) {
				throw redirect(303, '/not-found')
			}
		}
		throw e
	}
}

export const handleError: HandleServerError = ({ error }) => {
	if (error instanceof Error && error.message.includes('Not found')) {
		throw redirect(303, '/not-found')
	}
	return {
		message: 'Whoops!',
		code: error instanceof Error ? error.message : 'UNKNOWN'
	}
}
