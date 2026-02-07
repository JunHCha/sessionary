import type { Route, Page } from '@playwright/test'
import type {
	UserRead,
	OAuth2AuthorizeResponse,
	LectureAccessStatus,
	LectureDetail,
	SessionDetailResponse
} from '$lib/api/client/types.gen'

export const COOKIE_NAME = 'satk'
export const TEST_TOKEN = 'test-auth-token-12345'
export const TEST_CODE = 'test-oauth-code'
export const TEST_STATE = 'test-oauth-state'
export const API_BASE_URL = 'http://localhost:8000'

export function createDummyUser(): UserRead {
	return {
		id: '123e4567-e89b-12d3-a456-426614174000',
		email: 'test@example.com',
		nickname: 'Test User',
		is_active: true,
		is_superuser: false,
		is_verified: true,
		is_artist: false
	}
}

export function createDummyLecture(): LectureDetail {
	return {
		id: 1,
		title: 'Test Lecture',
		description: 'Test Description',
		thumbnail: 'https://example.com/thumb.jpg',
		artist: null,
		tags: null,
		length_sec: 300,
		lecture_count: 1,
		time_created: '2024-01-01T00:00:00Z',
		time_updated: '2024-01-01T00:00:00Z',
		lessons: [
			{
				id: 1,
				title: 'Session 1',
				length_sec: 300,
				lecture_ordering: 1,
				time_created: '2024-01-01T00:00:00Z',
				time_updated: '2024-01-01T00:00:00Z'
			}
		]
	}
}

export function createMockSessionDetailResponse(
	overrides: Partial<SessionDetailResponse> = {}
): SessionDetailResponse {
	return {
		id: 1,
		title: 'Test Session',
		session_type: 'PLAY',
		session_type_label: 'Play',
		lecture_ordering: 1,
		length_sec: 300,
		lecture: { id: 1, title: 'Test Lecture', total_sessions: 3 },
		video: {
			url: 'https://example.com/video.m3u8',
			type: 'hls',
			expires_at: '2025-12-31T23:59:59Z'
		},
		sheetmusic_url: null,
		sync_offset: 0,
		subtitles: [],
		playing_guide: [],
		navigation: { prev_session_id: null, next_session_id: 2 },
		...overrides
	}
}

export function mockUserMeApi(page: Page, dummyUser: UserRead = createDummyUser()) {
	page.route('**/user/me*', async (route: Route) => {
		const cookies = route.request().headers()['cookie'] || ''
		const hasToken = cookies.includes(`${COOKIE_NAME}=`)

		if (!hasToken) {
			await route.fulfill({
				status: 401,
				contentType: 'application/json',
				body: JSON.stringify({ detail: 'Missing token or inactive user.' })
			})
			return
		}

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(dummyUser)
		})
	})
}

export function mockAuthorizeApi(page: Page, shouldFail = false) {
	page.route('**/user/oauth/google/authorize*', async (route: Route) => {
		if (shouldFail) {
			await route.fulfill({
				status: 422,
				contentType: 'application/json',
				body: JSON.stringify({ detail: 'Validation Error' })
			})
			return
		}

		const response: OAuth2AuthorizeResponse = {
			authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?test=true'
		}

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(response)
		})
	})
}

export function mockCallbackApi(page: Page, shouldFail = false) {
	page.route('**/user/oauth/google/callback*', async (route: Route) => {
		if (shouldFail) {
			await route.fulfill({
				status: 400,
				contentType: 'application/json',
				body: JSON.stringify({ detail: 'Bad Request' })
			})
			return
		}

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			headers: {
				'Set-Cookie': `${COOKIE_NAME}=${TEST_TOKEN}; Path=/; HttpOnly; SameSite=Lax`
			},
			body: JSON.stringify({})
		})
	})
}

export function mockLectureApi(page: Page, lecture: LectureDetail = createDummyLecture()) {
	page.route(`${API_BASE_URL}/lecture/${lecture.id}`, async (route: Route) => {
		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ data: lecture })
		})
	})
}

export function mockTicketAccessApi(page: Page, hasAccess: boolean, ticketCount = 3) {
	page.route(`${API_BASE_URL}/ticket/lecture/*`, async (route: Route) => {
		const cookies = route.request().headers()['cookie'] || ''
		const hasToken = cookies.includes(`${COOKIE_NAME}=`)

		if (!hasToken) {
			await route.fulfill({
				status: 401,
				contentType: 'application/json',
				body: JSON.stringify({ detail: 'Unauthorized' })
			})
			return
		}

		const response: LectureAccessStatus = {
			accessible: hasAccess,
			ticket_count: ticketCount,
			reason: hasAccess ? 'unlimited' : undefined,
			expires_at: hasAccess ? '2024-01-08T00:00:00Z' : undefined
		}

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(response)
		})
	})
}

export function mockSessionDetailApi(
	page: Page,
	responseOrStatus: SessionDetailResponse | 401 | 403 | 404
) {
	page.route(`${API_BASE_URL}/session/*`, async (route: Route) => {
		if (typeof responseOrStatus === 'number') {
			const messages: Record<number, string> = {
				401: 'Unauthorized',
				403: 'Access denied',
				404: 'Session not found'
			}
			await route.fulfill({
				status: responseOrStatus,
				contentType: 'application/json',
				body: JSON.stringify({ detail: messages[responseOrStatus] })
			})
			return
		}

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(responseOrStatus)
		})
	})
}

export function mockAllOAuthApis(
	page: Page,
	options: { authorizeFail?: boolean; callbackFail?: boolean } = {}
) {
	mockAuthorizeApi(page, options.authorizeFail)
	mockCallbackApi(page, options.callbackFail)
	mockUserMeApi(page)
}
