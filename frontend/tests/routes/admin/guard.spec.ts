import { test, expect } from '@playwright/test'

test('비로그인 사용자는 /admin 접근 시 /home으로 리다이렉트', async ({ page }) => {
	await page.route('**/user/me*', (route) =>
		route.fulfill({
			status: 401,
			contentType: 'application/json',
			body: JSON.stringify({ detail: 'Unauthorized' })
		})
	)
	await page.goto('/admin')
	await expect(page).toHaveURL(/\/home/)
})

test('비관리자 사용자는 /admin 접근 시 /home으로 리다이렉트', async ({ page }) => {
	await page.route('**/user/me*', (route) =>
		route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({
				id: '1',
				nickname: 'u',
				email: 'u@u.com',
				is_artist: false,
				is_superuser: false
			})
		})
	)
	await page.goto('/admin')
	await expect(page).toHaveURL(/\/home/)
})

test('관리자는 /admin 진입 가능', async ({ page }) => {
	await page.route('**/user/me*', (route) =>
		route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({
				id: '1',
				nickname: 'admin',
				email: 'a@a.com',
				is_artist: false,
				is_superuser: true
			})
		})
	)
	await page.goto('/admin')
	await page.waitForLoadState('load')
	await expect(page.getByTestId('admin-hub')).toBeVisible({ timeout: 15000 })
})
