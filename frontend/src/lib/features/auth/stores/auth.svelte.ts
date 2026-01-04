import { writable } from 'svelte/store'

export const isAuthenticated = writable(false)

let _authenticated = $state(false)

isAuthenticated.subscribe((value) => {
	_authenticated = value
})

/**
 * 현재 모듈의 인증 상태에 대한 읽기 전용 접근자를 제공한다.
 *
 * @returns `isAuthenticated` 게터를 가진 객체. `isAuthenticated`는 인증되어 있으면 `true`, 그렇지 않으면 `false`를 반환한다.
 */
export function useAuth() {
	return {
		get isAuthenticated() {
			return _authenticated
		}
	}
}