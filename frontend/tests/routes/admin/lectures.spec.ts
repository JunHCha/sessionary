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

function lectureDetail(id: number, title: string, description = 'desc') {
	return {
		id,
		title,
		artist: null,
		lessons: [],
		description,
		thumbnail: null,
		tags: null,
		length_sec: 0,
		lecture_count: 0,
		time_created: '2024-01-01T00:00:00Z',
		time_updated: '2024-01-01T00:00:00Z'
	}
}

test.describe('admin 렉처 목록/생성', () => {
	test.beforeEach(async ({ page }) => {
		await mockAdminUser(page)
		await page.route('**/lecture', async (route) => {
			if (route.request().method() === 'POST') {
				const body = route.request().postDataJSON()
				await route.fulfill({
					status: 201,
					contentType: 'application/json',
					body: JSON.stringify({ data: lectureDetail(99, body.title, body.description) })
				})
				return
			}
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					data: [lectureInList(1, '기존 렉처')],
					meta: { page: 1, per_page: 20, total: 1 }
				})
			})
		})
	})

	test('목록을 렌더링한다', async ({ page }) => {
		await page.goto('/admin/lectures')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('lecture-row').first()).toContainText('기존 렉처', {
			timeout: 15000
		})
	})

	test('새 렉처를 생성하면 목록에 추가된다', async ({ page }) => {
		await page.goto('/admin/lectures')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('lecture-title-input')).toBeVisible({ timeout: 15000 })
		await page.getByTestId('lecture-title-input').fill('새 렉처')
		await page.getByTestId('create-lecture-btn').click()
		await expect(page.getByTestId('lecture-row')).toHaveCount(2)
		await expect(page.getByTestId('lecture-row').first()).toContainText('새 렉처')
	})
})

test.describe('admin 렉처 편집', () => {
	test.beforeEach(async ({ page }) => {
		await mockAdminUser(page)
		await page.route('**/lecture/1', async (route) => {
			if (route.request().method() === 'PATCH') {
				const body = route.request().postDataJSON()
				await route.fulfill({
					status: 200,
					contentType: 'application/json',
					body: JSON.stringify({
						data: lectureDetail(1, body.title ?? '렉처1', body.description ?? 'desc')
					})
				})
				return
			}
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({ data: lectureDetail(1, '렉처1') })
			})
		})
	})

	test('상세를 로드하고 제목을 수정 저장한다', async ({ page }) => {
		await page.goto('/admin/lectures/1')
		await page.waitForLoadState('load')
		const input = page.getByTestId('edit-title-input')
		await expect(input).toHaveValue('렉처1', { timeout: 15000 })
		await input.fill('수정된 제목')
		await page.getByTestId('save-lecture-btn').click()
		await expect(page.getByTestId('save-status')).toContainText('저장됨')
	})
})
