import { writable } from 'svelte/store'

export const isAuthenticated = writable(false)

let _authenticated = $state(false)

isAuthenticated.subscribe((value) => {
	_authenticated = value
})

export function useAuth() {
	return {
		get isAuthenticated() {
			return _authenticated
		}
	}
}
