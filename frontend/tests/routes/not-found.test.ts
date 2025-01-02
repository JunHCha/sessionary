import { expect, test } from '@playwright/test'

test.describe('404 page', () => {
	test('should display 404 page', async ({ page }) => {
		await page.goto('/something-invalid-route')
		await expect(page.locator('h1')).toHaveText('404')
	})
})
