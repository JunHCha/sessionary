import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAuth, setCurrentUser } from '$lib/features/auth'

vi.mock('$lib/api', () => ({
	usersCurrentUserUserMeGet: vi.fn()
}))

import { usersCurrentUserUserMeGet } from '$lib/api'

describe('OAuth 콜백 사용자 동기화', () => {
	beforeEach(() => {
		setCurrentUser(null)
		vi.clearAllMocks()
	})

	it('superuser 응답을 store에 반영하면 isAdmin과 isAuthenticated가 true', async () => {
		vi.mocked(usersCurrentUserUserMeGet).mockResolvedValue({
			nickname: 'admin',
			email: 'admin@a.com',
			is_artist: false,
			is_superuser: true
		} as never)

		const { fetchAndStoreCurrentUser } = await import(
			'../../../../src/routes/oauth-callback/+page.svelte'
		)
		await fetchAndStoreCurrentUser()

		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(true)
		expect(auth.isAdmin).toBe(true)
	})

	it('일반 사용자 응답이면 isAuthenticated는 true, isAdmin은 false', async () => {
		vi.mocked(usersCurrentUserUserMeGet).mockResolvedValue({
			nickname: 'user',
			email: 'user@a.com',
			is_artist: true,
			is_superuser: false
		} as never)

		const { fetchAndStoreCurrentUser } = await import(
			'../../../../src/routes/oauth-callback/+page.svelte'
		)
		await fetchAndStoreCurrentUser()

		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(true)
		expect(auth.isAdmin).toBe(false)
	})
})
