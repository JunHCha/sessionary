import { expect, test } from '@playwright/test'
import type { Route } from '@playwright/test'
import {
	TEST_CODE,
	TEST_STATE,
	mockLectureApi,
	mockTicketAccessApi,
	mockAuthorizeApi,
	mockCallbackApi,
	mockUserMeApi
} from '../../helpers/api-mocks'

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
