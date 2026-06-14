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

function lessonDetail(overrides: Record<string, unknown> = {}) {
	return {
		id: 5,
		lecture_id: 1,
		title: '레슨 A',
		length_sec: 0,
		text: '',
		lecture_ordering: 0,
		session_type: 'PLAY',
		sheetmusic_url: null,
		video_url: null,
		sync_offset: 0,
		subtitles: [],
		playing_guide: [],
		...overrides
	}
}

test.describe('admin 레슨 생성', () => {
	test.beforeEach(async ({ page }) => {
		await mockAdminUser(page)
		await page.route('**/lesson', async (route) => {
			const body = route.request().postDataJSON()
			await route.fulfill({
				status: 201,
				contentType: 'application/json',
				body: JSON.stringify({
					data: lessonDetail({
						id: 5,
						title: body.title,
						session_type: body.session_type,
						lecture_id: body.lecture_id
					})
				})
			})
		})
	})

	test('새 레슨을 생성하면 편집 페이지로 이동한다', async ({ page }) => {
		await page.goto('/admin/lessons/new?lectureId=1')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('lesson-title-input')).toBeVisible({ timeout: 15000 })
		await page.getByTestId('lesson-title-input').fill('레슨 A')
		await page.getByTestId('create-lesson-btn').click()
		await expect(page).toHaveURL(/\/admin\/lessons\/5/)
		await expect(page.getByTestId('lesson-editor')).toBeVisible({ timeout: 15000 })
	})
})

test.describe('admin 레슨 편집', () => {
	test.beforeEach(async ({ page }) => {
		await mockAdminUser(page)
		await page.route('**/lesson', async (route) => {
			const body = route.request().postDataJSON()
			await route.fulfill({
				status: 201,
				contentType: 'application/json',
				body: JSON.stringify({
					data: lessonDetail({ id: 5, title: body.title, lecture_id: body.lecture_id })
				})
			})
		})
		await page.route('**/lesson/5/video', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({ data: lessonDetail({ video_url: 'lesson-5/clip.mp4' }) })
			})
		})
		await page.route('**/lesson/5/sheetmusic', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({ data: lessonDetail({ sheetmusic_url: 'lesson-5/tab.xml' }) })
			})
		})
		await page.route('**/lesson/5', async (route) => {
			if (route.request().method() === 'PATCH') {
				const body = route.request().postDataJSON()
				await route.fulfill({
					status: 200,
					contentType: 'application/json',
					body: JSON.stringify({
						data: lessonDetail({ subtitles: body.subtitles ?? [] })
					})
				})
			} else {
				await route.fallback()
			}
		})
	})

	async function gotoEditor(page: Page) {
		await page.goto('/admin/lessons/new?lectureId=1')
		await page.waitForLoadState('load')
		await expect(page.getByTestId('lesson-title-input')).toBeVisible({ timeout: 15000 })
		await page.getByTestId('lesson-title-input').fill('레슨 A')
		await page.getByTestId('create-lesson-btn').click()
		await expect(page.getByTestId('lesson-editor')).toBeVisible({ timeout: 15000 })
	}

	test('자막 파일을 업로드하면 표에 행이 렌더되고 저장된다', async ({ page }) => {
		await gotoEditor(page)
		await page.getByTestId('subtitle-file').setInputFiles({
			name: 'sub.srt',
			mimeType: 'text/plain',
			buffer: Buffer.from('1\n00:00:00,000 --> 00:00:02,000\n안녕')
		})
		await expect(page.getByTestId('subtitle-row')).toHaveCount(1)
		await page.getByTestId('save-lesson-btn').click()
		await expect(page.getByTestId('lesson-save-status')).toContainText('저장됨')
	})

	test('동영상 파일을 업로드하면 업로드 호출이 성공한다', async ({ page }) => {
		await gotoEditor(page)
		await page.getByTestId('video-upload-input').setInputFiles({
			name: 'clip.mp4',
			mimeType: 'video/mp4',
			buffer: Buffer.from('binary')
		})
		await page.getByTestId('video-upload-btn').click()
		await expect(page.getByTestId('video-upload-status')).toContainText('완료')
	})
})
