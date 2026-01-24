import { expect, test } from '@playwright/test'
import type { Route, Page } from '@playwright/test'

function createMockLecture() {
	return {
		id: 1,
		title: 'Test Lecture',
		description: 'Test Description',
		artist_name: 'Test Artist',
		category: 'drums',
		thumbnail_url: 'https://example.com/thumb.jpg',
		lessons: [
			{ lesson_id: 1, title: 'Session 1', length_sec: 300, lecture_ordering: 1 },
			{ lesson_id: 2, title: 'Session 2', length_sec: 400, lecture_ordering: 2 }
		]
	}
}

async function mockApis(page: Page) {
	// 백엔드 API 요청만 mock (localhost:8000)
	await page.route('**/localhost:8000/lecture/*', async (route: Route) => {
		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ data: createMockLecture() })
		})
	})

	await page.route('**/localhost:8000/user/me*', async (route: Route) => {
		await route.fulfill({
			status: 401,
			contentType: 'application/json',
			body: JSON.stringify({ detail: 'Unauthorized' })
		})
	})
}

test.describe('Session 클릭 시 로그인 유도', () => {
	test.beforeEach(async ({ page, context }) => {
		await context.clearCookies()
	})

	test('비로그인 상태에서 SessionItem 클릭 시 LoginModal이 표시된다', async ({ page }) => {
		await mockApis(page)

		await page.goto('/lecture/1')

		const sessionItem = page.locator('[data-testid="session-item"]').first()
		await expect(sessionItem).toBeVisible({ timeout: 10000 })
		await sessionItem.click()

		const loginModal = page.locator('text=Sign in with Google')
		await expect(loginModal).toBeVisible({ timeout: 5000 })
	})

	test('로그인 모달에 세션 접근 안내 메시지가 표시된다', async ({ page }) => {
		await mockApis(page)

		await page.goto('/lecture/1')

		const sessionItem = page.locator('[data-testid="session-item"]').first()
		await expect(sessionItem).toBeVisible({ timeout: 10000 })
		await sessionItem.click()

		const message = page.locator('text=세션을 시청하려면 로그인이 필요합니다')
		await expect(message).toBeVisible({ timeout: 5000 })
	})

	test('세션 클릭 시 pendingAction이 저장된다', async ({ page }) => {
		await mockApis(page)

		await page.goto('/lecture/1')

		const sessionItem = page.locator('[data-testid="session-item"]').first()
		await expect(sessionItem).toBeVisible({ timeout: 10000 })
		await sessionItem.click()

		// sessionStorage 확인
		const pendingAction = await page.evaluate(() => sessionStorage.getItem('pendingAction'))
		expect(pendingAction).not.toBeNull()
		const parsed = JSON.parse(pendingAction!)
		expect(parsed.type).toBe('access-session')
		expect(parsed.sessionId).toBe(1)
	})

	test('Google 로그인 버튼 클릭 시 redirectUrl이 현재 페이지로 저장된다', async ({ page }) => {
		await mockApis(page)

		let capturedRedirectUrl: string | null = null

		// Google OAuth authorize API mock - redirectUrl 캡처
		await page.route('**/localhost:8000/user/oauth/google/authorize*', async (route) => {
			// API 호출 시점에서 sessionStorage 값을 캡처
			capturedRedirectUrl = await route.request().frame()?.page()?.evaluate(
				() => sessionStorage.getItem('redirectUrl')
			) ?? null

			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?test=true'
				})
			})
		})

		await page.goto('/lecture/1')

		const sessionItem = page.locator('[data-testid="session-item"]').first()
		await expect(sessionItem).toBeVisible({ timeout: 10000 })
		await sessionItem.click()

		const googleButton = page.locator('button:has-text("Sign in with Google")')
		await expect(googleButton).toBeVisible({ timeout: 5000 })
		await googleButton.click()

		// API가 호출될 때까지 대기
		await page.waitForResponse('**/localhost:8000/user/oauth/google/authorize*')

		// redirectUrl 저장 확인
		expect(capturedRedirectUrl).toBe('/lecture/1')
	})
})
