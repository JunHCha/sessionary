import { expect, test } from '@playwright/test'
import { test as authTest, expect as authExpect } from '../../fixtures/auth'
import {
	COOKIE_NAME,
	createMockSessionDetailResponse,
	mockSessionDetailApi,
	mockUserMeApi
} from '../../helpers/api-mocks'

test.describe('Session Detail 페이지 Type 1 레이아웃', () => {
	test.beforeEach(async ({ page }) => {
		mockUserMeApi(page)
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

test.describe('Session Detail Mock 인프라 검증', () => {
	test.beforeEach(async ({ page }) => {
		mockUserMeApi(page)
		await page.goto('/session/1')
	})

	test('mockSessionDetailApi가 200 응답을 올바르게 설정합니다', async ({ page }) => {
		const mockResponse = createMockSessionDetailResponse({ title: 'Mock Session' })
		mockSessionDetailApi(page, mockResponse)

		const result = await page.evaluate(async () => {
			const res = await fetch('http://localhost:8000/session/1')
			return { status: res.status, body: await res.json() }
		})

		expect(result.status).toBe(200)
		expect(result.body.title).toBe('Mock Session')
	})

	test('mockSessionDetailApi가 401 응답을 올바르게 설정합니다', async ({ page }) => {
		mockSessionDetailApi(page, 401)

		const result = await page.evaluate(async () => {
			const res = await fetch('http://localhost:8000/session/1')
			return { status: res.status, body: await res.json() }
		})

		expect(result.status).toBe(401)
		expect(result.body.detail).toBe('Unauthorized')
	})

	test('mockSessionDetailApi가 403 응답을 올바르게 설정합니다', async ({ page }) => {
		mockSessionDetailApi(page, 403)

		const result = await page.evaluate(async () => {
			const res = await fetch('http://localhost:8000/session/1')
			return { status: res.status, body: await res.json() }
		})

		expect(result.status).toBe(403)
		expect(result.body.detail).toBe('Access denied')
	})

	test('mockSessionDetailApi가 404 응답을 올바르게 설정합니다', async ({ page }) => {
		mockSessionDetailApi(page, 404)

		const result = await page.evaluate(async () => {
			const res = await fetch('http://localhost:8000/session/1')
			return { status: res.status, body: await res.json() }
		})

		expect(result.status).toBe(404)
		expect(result.body.detail).toBe('Session not found')
	})
})

authTest.describe('Session Detail 인증 Fixture 검증', () => {
	authTest('authenticatedPage fixture가 쿠키를 올바르게 설정합니다', async ({
		authenticatedPage
	}) => {
		const cookies = await authenticatedPage.context().cookies()
		const authCookie = cookies.find((c) => c.name === COOKIE_NAME)

		authExpect(authCookie).toBeDefined()
		authExpect(authCookie!.value).toBeTruthy()
	})

	authTest('unauthenticatedPage fixture에 인증 쿠키가 없습니다', async ({
		unauthenticatedPage
	}) => {
		const cookies = await unauthenticatedPage.context().cookies()
		const authCookie = cookies.find((c) => c.name === COOKIE_NAME)

		authExpect(authCookie).toBeUndefined()
	})

	authTest('authenticatedPage로 페이지 로드 시 user/me가 200을 반환합니다', async ({
		authenticatedPage
	}) => {
		const responsePromise = authenticatedPage.waitForResponse('**/user/me*')
		await authenticatedPage.goto('/session/1')
		const response = await responsePromise

		authExpect(response.status()).toBe(200)
		const body = await response.json()
		authExpect(body.nickname).toBe('Test User')
	})

	authTest('unauthenticatedPage로 페이지 로드 시 user/me가 401을 반환합니다', async ({
		unauthenticatedPage
	}) => {
		const responsePromise = unauthenticatedPage.waitForResponse('**/user/me*')
		await unauthenticatedPage.goto('/session/1')
		const response = await responsePromise

		authExpect(response.status()).toBe(401)
	})
})
