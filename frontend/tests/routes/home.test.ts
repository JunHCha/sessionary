import { expect, test } from '@playwright/test'

test.describe('Home page navigation bar', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('should redirect to home when entering /', async ({ page }) => {
		try {
			await page.goto('/', { waitUntil: 'networkidle' })
		} catch (error) {
			console.log('Navigation interrupted, continuing...', error)
		}
		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')
	})

	test('should display the navigation bar', async ({ page }) => {
		const navbar = page.locator('[data-testid="navbar"]')
		await expect(navbar).toBeVisible()
	})

	test('should display login button with text', async ({ page }) => {
		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()
	})
})

test.describe('Home page contents', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('should have a hero section with main content', async ({ page }) => {
		const heroSection = page.locator('section .hero-section')
		await expect(heroSection).toBeVisible()
	})

	test('should have recommended lecture section', async ({ page }) => {
		const recommendedSection = page.locator('text=요즘 많이 보는 렉처')
		await expect(recommendedSection).toBeVisible()
	})

	test('should have new lecture section', async ({ page }) => {
		const newSection = page.locator('h2:has-text("새로운 렉쳐")')
		await expect(newSection).toBeVisible()
	})
})
