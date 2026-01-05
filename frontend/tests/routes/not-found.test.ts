import { expect, test } from '@playwright/test'

test.describe('404 페이지', () => {
	test('404 페이지를 표시합니다', async ({ page }) => {
		await page.goto('/something-invalid-route')
		await expect(page.locator('h1')).toHaveText('404')
	})
})
