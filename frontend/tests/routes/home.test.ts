import { expect, test } from '@playwright/test'

test.describe('홈 페이지 네비게이션 바', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('/로 접근 시 home으로 리다이렉트됩니다', async ({ page }) => {
		try {
			await page.goto('/', { waitUntil: 'networkidle' })
		} catch (error) {
			console.log('Navigation interrupted, continuing...', error)
		}
		await page.waitForURL('**/home')
		expect(page.url()).toContain('/home')
	})

	test('네비게이션 바를 표시합니다', async ({ page }) => {
		const navbar = page.locator('[data-testid="navbar"]')
		await expect(navbar).toBeVisible()
	})

	test('로그인 버튼을 텍스트와 함께 표시합니다', async ({ page }) => {
		const loginButton = page.locator('[data-testid="login-button"]')
		await expect(loginButton).toBeVisible()
	})
})

test.describe('홈 페이지 콘텐츠', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/home')
	})

	test('메인 콘텐츠가 있는 hero 섹션을 가집니다', async ({ page }) => {
		const heroSection = page.locator('section .hero-section')
		await expect(heroSection).toBeVisible()
	})

	test('추천 렉처 섹션을 가집니다', async ({ page }) => {
		const recommendedSection = page.locator('text=요즘 많이 보는 렉처')
		await expect(recommendedSection).toBeVisible()
	})

	test('새로운 렉처 섹션을 가집니다', async ({ page }) => {
		const newSection = page.locator('h2:has-text("새로운 렉쳐")')
		await expect(newSection).toBeVisible()
	})
})
