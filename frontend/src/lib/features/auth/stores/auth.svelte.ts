import type { UserRead } from '$lib/api'

let isAuthenticated = $state(false)
let currentUser = $state<UserRead | null>(null)

export function setIsAuthenticated(value: boolean) {
	isAuthenticated = value
}

export function setCurrentUser(user: UserRead | null) {
	currentUser = user
	isAuthenticated = user !== null
}

export function useAuth() {
	return {
		get isAuthenticated() {
			return isAuthenticated
		},
		get user() {
			return currentUser
		},
		get isAdmin() {
			return currentUser?.is_superuser === true
		}
	}
}
