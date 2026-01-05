let isAuthenticated = $state(false)

export function setIsAuthenticated(value: boolean) {
	isAuthenticated = value
}

export function useAuth() {
	return {
		get isAuthenticated() {
			return isAuthenticated
		}
	}
}
