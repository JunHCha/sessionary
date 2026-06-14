import { test, expect } from '@playwright/test'

function mockAdmin(page: import('@playwright/test').Page) {
	return page.route('**/user/me', (route) =>
		route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({
				id: 'admin-id',
				email: 'admin@sessionary.com',
				is_active: true,
				is_superuser: true,
				is_verified: true,
				nickname: 'admin',
				is_artist: true
			})
		})
	)
}

const emptyCuration = { data: { TRENDING: [], NEW: [] } }
const emptyLectures = {
	data: [],
	meta: { total_items: 0, total_pages: 1, curr_page: 1, per_page: 20 }
}

test('admin에서는 전역 navbar가 숨겨진다', async ({ page }) => {
	await mockAdmin(page)
	await page.route('**/curation', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyCuration) })
	)
	await page.route('**/lecture**', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyLectures) })
	)
	await page.goto('/admin')
	await expect(page.getByTestId('admin-shell')).toBeVisible()
	await expect(page.getByTestId('navbar')).toHaveCount(0)
})

test('admin에서 사이트로 돌아가기 후 /home에 navbar가 다시 보인다', async ({ page }) => {
	await mockAdmin(page)
	await page.route('**/curation', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyCuration) })
	)
	await page.route('**/lecture**', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyLectures) })
	)
	await page.goto('/admin')
	await expect(page.getByTestId('admin-shell')).toBeVisible()

	await page.getByRole('link', { name: '사이트로 돌아가기' }).first().click()
	await page.waitForURL('**/home')
	const navbar = page.getByTestId('navbar')
	await expect(navbar).toBeVisible()
	// opacity-0 / -translate-y-full 같은 "숨김" 상태까지 잡아낸다
	await expect(navbar).toBeInViewport()
	const opacity = await navbar.evaluate((el) => getComputedStyle(el).opacity)
	expect(Number(opacity)).toBeGreaterThan(0.5)
})

test('모바일에서 admin → 사이트로 돌아가기 후 navbar가 보인다', async ({ page }) => {
	await page.setViewportSize({ width: 390, height: 800 })
	await mockAdmin(page)
	await page.route('**/curation', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyCuration) })
	)
	await page.route('**/lecture**', (r) =>
		r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(emptyLectures) })
	)
	await page.goto('/admin')
	await expect(page.getByTestId('admin-shell')).toBeVisible()
	await page.getByRole('button', { name: '메뉴' }).click()
	await page.getByRole('link', { name: '사이트로 돌아가기' }).click()
	await page.waitForURL('**/home')
	await expect(page.getByTestId('navbar')).toBeInViewport()
})
