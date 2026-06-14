import { test, expect, type Page } from '@playwright/test'

function mockAdminUser(page: Page) {
	return page.route('**/user/me*', (route) =>
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
}

function lectureInList(id: number, title: string) {
	return {
		id,
		thumbnail: null,
		title,
		artist: null,
		lessons: [],
		description: 'desc',
		tags: null,
		length_sec: 0,
		lecture_count: 0,
		time_created: '2024-01-01T00:00:00Z',
		time_updated: '2024-01-01T00:00:00Z'
	}
}

test.describe('admin 큐레이션', () => {
	test.beforeEach(async ({ page }) => {
		await mockAdminUser(page)
		await page.route('**/lecture', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					data: [
						lectureInList(1, '렉처 1'),
						lectureInList(2, '렉처 2'),
						lectureInList(3, '렉처 3')
					],
					meta: { page: 1, per_page: 20, total: 3 }
				})
			})
		})
		// API 요청(/curation, /curation/{section})만 가로채고
		// SvelteKit 페이지 경로(/admin/curation)는 통과시킨다.
		await page.route(
			(url) =>
				/\/curation(\/[^/]+)?$/.test(url.pathname) && !url.pathname.includes('/admin/'),
			async (route) => {
				const pathname = new URL(route.request().url()).pathname
				const isSection = /\/curation\/[^/]+$/.test(pathname)
				if (isSection) {
					await route.fulfill({
						status: 200,
						contentType: 'application/json',
						body: '{"ok":true}'
					})
					return
				}
				await route.fulfill({
					status: 200,
					contentType: 'application/json',
					body: JSON.stringify({ data: { TRENDING: [], NEW: [] } })
				})
			}
		)
	})

	test('후보를 TRENDING에 추가하고 저장하면 순서대로 PUT된다', async ({ page }) => {
		await page.goto('/admin/curation')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('candidate-1')).toBeVisible({ timeout: 15000 })

		await page.getByTestId('add-to-TRENDING-3').click()
		await page.getByTestId('add-to-TRENDING-1').click()

		await expect(page.getByTestId('section-TRENDING').getByTestId('selected-item')).toHaveCount(
			2
		)

		const putRequest = page.waitForRequest(
			(req) =>
				req.method() === 'PUT' && /\/curation\/TRENDING$/.test(new URL(req.url()).pathname)
		)
		await page.getByTestId('save-TRENDING-btn').click()
		const req = await putRequest
		expect(req.postDataJSON().lecture_ids).toEqual([3, 1])
	})

	test('선택 항목을 위로 이동하면 순서가 바뀐다', async ({ page }) => {
		await page.goto('/admin/curation')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('candidate-1')).toBeVisible({ timeout: 15000 })
		await page.getByTestId('add-to-NEW-1').click()
		await page.getByTestId('add-to-NEW-2').click()
		await page.getByTestId('move-up-NEW-1').click()

		const putRequest = page.waitForRequest(
			(req) => req.method() === 'PUT' && /\/curation\/NEW$/.test(new URL(req.url()).pathname)
		)
		await page.getByTestId('save-NEW-btn').click()
		const req = await putRequest
		expect(req.postDataJSON().lecture_ids).toEqual([2, 1])
	})
})
