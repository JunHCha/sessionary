import { test as base, type Page } from '@playwright/test'
import {
	COOKIE_NAME,
	TEST_TOKEN,
	createDummyUser,
	mockUserMeApi
} from '../helpers/api-mocks'
import type { UserRead } from '$lib/api/client/types.gen'

type AuthFixtures = {
	authenticatedPage: Page
	unauthenticatedPage: Page
}

export const test = base.extend<AuthFixtures>({
	authenticatedPage: async ({ page, context }, use) => {
		await context.addCookies([
			{
				name: COOKIE_NAME,
				value: TEST_TOKEN,
				domain: 'localhost',
				path: '/'
			}
		])
		mockUserMeApi(page, createDummyUser())
		await use(page)
	},

	unauthenticatedPage: async ({ page, context }, use) => {
		await context.clearCookies()
		mockUserMeApi(page)
		await use(page)
	}
})

export { expect } from '@playwright/test'
