import { expect, test } from '@playwright/test'
import type { Route, Page } from '@playwright/test'
import type {
	UserRead,
	OAuth2AuthorizeResponse,
	LectureAccessStatus,
	LectureDetail
} from '$lib/api/client/types.gen'

const COOKIE_NAME = 'satk'
const TEST_TOKEN = 'test-auth-token-12345'
const TEST_CODE = 'test-oauth-code'
const TEST_STATE = 'test-oauth-state'

function createDummyUser(): UserRead {
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

function createDummyLecture(): LectureDetail {
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

function mockLectureApi(page: Page) {
	page.route('http://localhost:8000/lecture/1', async (route: Route) => {
		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ data: createDummyLecture() })
		})
	})
}

function mockTicketAccessApi(page: Page, hasAccess: boolean, ticketCount = 3) {
	page.route('http://localhost:8000/ticket/lecture/1', async (route: Route) => {
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

function mockAuthorizeApi(page: Page) {
	page.route('**/user/oauth/google/authorize*', async (route: Route) => {
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

function mockCallbackApi(page: Page) {
	page.route('**/user/oauth/google/callback*', async (route: Route) => {
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

function mockUserMeApi(page: Page, dummyUser: UserRead = createDummyUser()) {
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

test.describe('미인증 사용자 세션 접근', () => {
	test.beforeEach(async ({ context }) => {
		await context.clearCookies()
	})

	test('미인증 사용자가 세션을 클릭하면 로그인 모달이 표시됩니다', async ({ page }) => {
		mockLectureApi(page)
		mockTicketAccessApi(page, false, 3)
		mockUserMeApi(page)

		await page.goto('/lecture/1')
		await page.waitForLoadState('load')

		// 세션 목록이 렌더링될 때까지 대기
		await page.locator('h2:has-text("세션 목록")').waitFor({ timeout: 15000 })

		const sessionItem = page.locator('button').filter({ hasText: 'Session 1' }).first()
		await expect(sessionItem).toBeVisible({ timeout: 15000 })
		await sessionItem.click()

		const loginModal = page.locator('text=로그인이 필요합니다')
		await expect(loginModal).toBeVisible({ timeout: 5000 })

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible()
	})

	test('로그인 후 티켓이 있으면 티켓 확인 모달이 표시됩니다', async ({ page }) => {
		mockLectureApi(page)
		mockTicketAccessApi(page, false, 3)
		mockAuthorizeApi(page)
		mockCallbackApi(page)
		mockUserMeApi(page)

		await page.goto('/lecture/1')
		await page.waitForLoadState('load')

		// 세션 목록이 렌더링될 때까지 대기
		await page.locator('h2:has-text("세션 목록")').waitFor({ timeout: 15000 })

		const sessionItem = page.locator('button').filter({ hasText: 'Session 1' }).first()
		await expect(sessionItem).toBeVisible({ timeout: 15000 })
		await sessionItem.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 5000 })

		// googleButton 클릭 시 authorize API가 호출되고 redirectUrl이 저장됨
		// pendingSessionId는 세션 클릭 시 자동으로 저장됨
		const authorizePromise = page.waitForResponse('**/user/oauth/google/authorize*')
		await googleButton.click()
		await authorizePromise

		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`)
		await page.waitForResponse('**/user/oauth/google/callback*')
		await page.waitForResponse('**/user/me*')
		await page.waitForURL('**/lecture/1')

		await page.waitForResponse('http://localhost:8000/ticket/lecture/1')

		const confirmModal = page.locator('text=티켓 1개를 사용하여 이 강의에 접근합니다')
		await expect(confirmModal).toBeVisible({ timeout: 10000 })

		const ticketCountText = page.locator('text=현재 보유 티켓 수: 3개')
		await expect(ticketCountText).toBeVisible()
	})

	test('로그인 후 무제한 구독이 있으면 바로 세션으로 이동합니다', async ({ page }) => {
		mockLectureApi(page)
		mockTicketAccessApi(page, true, 0)
		mockAuthorizeApi(page)
		mockCallbackApi(page)
		mockUserMeApi(page)

		// Google OAuth URL을 인터셉트하여 콜백으로 리다이렉트
		page.route('**/accounts.google.com/**', async (route: Route) => {
			await route.fulfill({
				status: 302,
				headers: {
					'Location': `/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`
				}
			})
		})

		page.route('**/session/1', async (route: Route) => {
			await route.fulfill({
				status: 200,
				contentType: 'text/html',
				body: '<html><body><div data-testid="session-detail-page">Session Detail</div></body></html>'
			})
		})

		await page.goto('/lecture/1')
		await page.waitForLoadState('load')

		// 세션 목록이 렌더링될 때까지 대기
		await page.locator('h2:has-text("세션 목록")').waitFor({ timeout: 15000 })

		const sessionItem = page.locator('button').filter({ hasText: 'Session 1' }).first()
		await expect(sessionItem).toBeVisible({ timeout: 15000 })
		await sessionItem.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 5000 })

		// googleButton 클릭 시 authorize API가 호출되고 redirectUrl이 저장됨
		// pendingSessionId는 세션 클릭 시 자동으로 저장됨
		const authorizePromise = page.waitForResponse('**/user/oauth/google/authorize*')
		await googleButton.click()
		await authorizePromise

		// 리다이렉트 대신 직접 콜백 페이지로 이동
		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`, { waitUntil: 'commit' })
		await page.waitForResponse('**/user/oauth/google/callback*')
		await page.waitForResponse('**/user/me*')
		await page.waitForURL('**/lecture/1')

		await page.waitForResponse('http://localhost:8000/ticket/lecture/1')

		await page.waitForURL('**/session/1', { timeout: 10000 })
		expect(page.url()).toContain('/session/1')
	})
})
