import { expect, test } from '@playwright/test'

test.describe('Home page navigation bar', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('should redirect to home when entering /', async ({ page }) => {
		await page.goto('/')
		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')
	})

	test('should display the navigation bar', async ({ page }) => {
		const navbar = page.locator('nav')
		await expect(navbar).toBeVisible()
	})

	test('should display login button with text', async ({ page }) => {
		const loginButton = page.locator('button:has-text("로그인/회원가입")')
		await expect(loginButton).toBeVisible()
	})
})

test.describe('Home page contents', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('should have a last seen section', async ({ page }) => {
		const lastSeenSection = page.locator('section:has-text("마지막으로 본 세션")')
		await expect(lastSeenSection).toBeVisible()
	})

	test('should have recommended and new lecture sections', async ({ page }) => {
		const recommendedSection = page.locator('section:has-text("추천하는 렉쳐")')
		await expect(recommendedSection).toBeVisible()

		const newSection = page.locator('section:has-text("새롭게 추가된 렉쳐")')
		await expect(newSection).toBeVisible()
	})
})

test.describe('404 page', () => {
	test('should display 404 page', async ({ page }) => {
		await page.goto('/something-invalid-route')
		await expect(page.locator('h1')).toHaveText('404')
	})
})
