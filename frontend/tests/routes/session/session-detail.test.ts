import { expect, test } from '@playwright/test'

test.describe('Session Detail 페이지 Type 1 레이아웃', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/session/1')
	})

	test('페이지가 정상적으로 로드됩니다', async ({ page }) => {
		const mainContainer = page.locator('[data-testid="session-detail-page"]')
		await expect(mainContainer).toBeVisible()
	})

	test('VideoPlayer가 표시됩니다', async ({ page }) => {
		const videoPlayer = page.locator('[data-testid="video-player"]')
		await expect(videoPlayer).toBeVisible()
	})

	test('SubtitlePanel placeholder가 표시됩니다', async ({ page }) => {
		const subtitlePanel = page.locator('[data-testid="subtitle-panel-placeholder"]')
		await expect(subtitlePanel).toBeVisible()
	})

	test('TabSheet placeholder가 표시됩니다', async ({ page }) => {
		const tabSheet = page.locator('[data-testid="tab-sheet-placeholder"]')
		await expect(tabSheet).toBeVisible()
	})

	test('PlayingGuide placeholder가 표시됩니다', async ({ page }) => {
		const playingGuide = page.locator('[data-testid="playing-guide-placeholder"]')
		await expect(playingGuide).toBeVisible()
	})

	test('세션 네비게이션이 표시됩니다', async ({ page }) => {
		const navigation = page.locator('[data-testid="session-navigation"]')
		await expect(navigation).toBeVisible()
	})
})
