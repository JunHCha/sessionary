import { expect, test } from '@playwright/test'
import type { Route } from '@playwright/test'
import {
	TEST_CODE,
	TEST_STATE,
	mockAuthorizeApi,
	mockCallbackApi,
	mockUserMeApi,
	mockAllOAuthApis
} from '../../helpers/api-mocks'

test.describe('Google OAuth Login', () => {
	test.beforeEach(async ({ page, context }) => {
		await context.clearCookies()
		await page.goto('/home')
		await page.reload()
	})

	test('OAuth login flow를 성공적으로 수행합니다', async ({ page }) => {
		// Google URL로의 navigation을 가로채서 /oauth-callback으로 리다이렉트
		await page.route('https://accounts.google.com/**', async (route) => {
			// Google로 가는 요청을 abort하고 대신 callback으로 이동하도록 함
			await route.abort()
		})

		mockAuthorizeApi(page, false)
		mockCallbackApi(page)
		mockUserMeApi(page)

		// user/me 응답 Promise를 미리 설정
		const userMeResponsePromise = page.waitForResponse('**/user/me*')

		await page.waitForLoadState('networkidle')

		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()
		await expect(loginButton).toBeEnabled()
		await loginButton.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 10000 })
		await expect(googleButton).toBeEnabled()

		// authorize API 응답을 기다리면서 클릭
		const authorizePromise = page.waitForResponse('**/user/oauth/google/authorize*')
		await googleButton.click()
		await authorizePromise

		// Google navigation이 abort되었으므로 직접 callback으로 이동
		await page.goto(`/oauth-callback?code=${TEST_CODE}&state=${TEST_STATE}`)

		// /home으로 리다이렉트될 때까지 대기
		await page.waitForURL('**/home', { timeout: 15000 })
		expect(page.url()).toContain('/home')

		// user/me API 응답 확인
		await userMeResponsePromise

		await expect(loginButton).not.toBeVisible()
		const logoutButton = page.locator('button:has-text("로그아웃")')
		await expect(logoutButton).toBeVisible({ timeout: 10000 })
	})

	test('authorize API 실패를 처리합니다', async ({ page }) => {
		mockAuthorizeApi(page, true)
		mockUserMeApi(page)

		await page.waitForLoadState('networkidle')

		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()
		await expect(loginButton).toBeEnabled()

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
