import { expect, test } from '@playwright/test'
import type { Route, Page } from '@playwright/test'
import type { UserRead, OAuth2AuthorizeResponse } from '$lib/api/client/types.gen'

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

function mockAuthorizeApi(page: Page, shouldFail = false, onMockCalled?: () => void) {
	page.route('**/user/oauth/google/authorize*', async (route: Route) => {
		if (onMockCalled) {
			onMockCalled()
		}

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

function mockCallbackApi(page: Page, shouldFail = false) {
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

function mockAllOAuthApis(
	page: Page,
	options: { authorizeFail?: boolean; callbackFail?: boolean } = {}
) {
	mockAuthorizeApi(page, options.authorizeFail)
	mockCallbackApi(page, options.callbackFail)
	mockUserMeApi(page)
}

test.describe('Google OAuth Login', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('OAuth login flow를 성공적으로 수행합니다', async ({ page }) => {
		mockAuthorizeApi(page, false)
		mockCallbackApi(page)
		mockUserMeApi(page)

		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()

		await page.waitForTimeout(500)
		await loginButton.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 10000 })

		await googleButton.click()

		await page.waitForTimeout(1000)

		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`)

		await page.waitForResponse('**/user/oauth/google/callback*')
		await page.waitForResponse('**/user/me*')

		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')

		await expect(loginButton).not.toBeVisible()
		const logoutButton = page.locator('button:has-text("로그아웃")')
		await expect(logoutButton).toBeVisible()
	})

	test('authorize API 실패를 처리합니다', async ({ page }) => {
		mockAuthorizeApi(page, true)

		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()
		await loginButton.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 10000 })

		const responsePromise = page.waitForResponse('**/user/oauth/google/authorize*')
		await googleButton.click()

		const response = await responsePromise
		expect(response.status()).toBe(422)
	})

	test('error 파라미터가 있는 callback을 처리합니다', async ({ page }) => {
		mockAllOAuthApis(page)

		await page.goto('/oauth-callback?error=access_denied')

		const alertPromise = page.waitForEvent('dialog')
		const alert = await alertPromise
		expect(alert.message()).toContain('로그인 중 오류가 발생했습니다')

		await alert.accept()
		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')
	})

	test('code와 state가 없는 callback을 처리합니다', async ({ page }) => {
		mockAllOAuthApis(page)

		await page.goto('/oauth-callback')

		const alertPromise = page.waitForEvent('dialog')
		const alert = await alertPromise
		expect(alert.message()).toContain('로그인 중 오류가 발생했습니다')

		await alert.accept()
		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')
	})

	test('callback API 실패를 처리합니다', async ({ page }) => {
		mockAuthorizeApi(page)
		mockCallbackApi(page, true)
		mockUserMeApi(page)

		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`)

		await page.waitForResponse('**/user/oauth/google/callback*')
		await page.waitForURL('**/not-found')
		expect(page.url()).toContain('/not-found')
	})

	test('token이 없을 때 user me API 실패를 처리합니다', async ({ page }) => {
		mockAuthorizeApi(page)

		page.route('**/user/oauth/google/callback*', async (route: Route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({})
			})
		})

		mockUserMeApi(page)

		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`)

		await page.waitForResponse('**/user/oauth/google/callback*')

		const response = await page.waitForResponse('**/user/me*')
		expect(response.status()).toBe(401)

		await page.waitForURL('**/not-found')
		expect(page.url()).toContain('/not-found')
	})
})
