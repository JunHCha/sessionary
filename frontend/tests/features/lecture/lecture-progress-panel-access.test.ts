import { expect, test } from '@playwright/test'
import {
	API_BASE_URL,
	COOKIE_NAME,
	TEST_TOKEN,
	mockLectureApi,
	mockTicketAccessApi,
	mockUserMeApi
} from '../../helpers/api-mocks'

test.describe('렉처 진행도 패널 - 접근상태 조회', () => {
	test('인증 사용자가 렉처에 진입해도 접근상태 API를 무한 호출하지 않는다', async ({
		page,
		context
	}) => {
		// 로그인 상태 재현: API 도메인에 세션 쿠키 주입 → /user/me 가 200 을 반환
		await context.addCookies([
			{ name: COOKIE_NAME, value: TEST_TOKEN, url: API_BASE_URL }
		])

		mockUserMeApi(page)
		mockLectureApi(page)
		mockTicketAccessApi(page, true, 0)

		let ticketCalls = 0
		page.on('request', (request) => {
			if (request.url().includes('/ticket/lecture/')) {
				ticketCalls++
			}
		})

		await page.goto('/lecture/1')
		await page.waitForLoadState('load')
		await page.locator('[data-testid="lecture-progress-panel"]').waitFor({ timeout: 15000 })

		// 반응성 루프가 있으면 이 대기 동안 수백 회 호출된다
		await page.waitForTimeout(2000)

		expect(ticketCalls).toBeLessThanOrEqual(1)
	})
})
