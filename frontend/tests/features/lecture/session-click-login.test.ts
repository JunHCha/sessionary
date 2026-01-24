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
})
