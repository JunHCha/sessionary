import { describe, it, expect, beforeEach } from 'vitest'
import { useAuth, setCurrentUser } from '$lib/features/auth/stores/auth.svelte'

describe('auth store', () => {
	beforeEach(() => setCurrentUser(null))

	it('비로그인 시 isAdmin은 false', () => {
		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(false)
		expect(auth.isAdmin).toBe(false)
	})

	it('superuser 사용자 설정 시 isAdmin true', () => {
		setCurrentUser({
			nickname: 'a',
			email: 'a@a.com',
			is_artist: false,
			is_superuser: true
		} as never)
		const auth = useAuth()
		expect(auth.isAuthenticated).toBe(true)
		expect(auth.isAdmin).toBe(true)
	})

	it('일반 사용자는 isAdmin false', () => {
		setCurrentUser({
			nickname: 'b',
			email: 'b@b.com',
			is_artist: true,
			is_superuser: false
		} as never)
		expect(useAuth().isAdmin).toBe(false)
	})
})
