import { OpenAPI } from './client'

let isInitialized = false
let resolveInit: (() => void) | null = null
const initPromise = new Promise<void>((resolve) => {
	resolveInit = resolve
})

/**
 * OpenAPI 클라이언트를 주어진 베이스 URL로 구성하고 인증 관련 옵션과 요청 인터셉터를 설정합니다.
 *
 * 동일한 베이스 URL로 이미 초기화되어 있으면 아무 작업도 수행하지 않습니다. 초기화가 완료되면 내부 대기 프라미스를 해제하여 대기 중인 호출자가 계속 진행할 수 있게 합니다.
 *
 * @param baseUrl - API 요청에 사용할 기본 URL
 */
export function initializeApi(baseUrl: string) {
	if (isInitialized && OpenAPI.BASE === baseUrl) {
		return
	}
	OpenAPI.BASE = baseUrl
	OpenAPI.WITH_CREDENTIALS = true
	OpenAPI.interceptors.request.use((request) => {
		request.withCredentials = true
		return request
	})
	isInitialized = true
	resolveInit?.()
}

/**
 * API 클라이언트 초기화가 완료될 때까지 대기한다.
 *
 * @returns 초기화가 완료되면 해결되는 빈 값
 */
export function waitForApiInit(): Promise<void> {
	if (isInitialized) return Promise.resolve()
	return initPromise
}

/**
 * API 클라이언트가 초기화되었는지 확인합니다.
 *
 * @returns `true`이면 초기화가 완료된 상태, `false`이면 아직 초기화되지 않은 상태
 */
export function isApiInitialized(): boolean {
	return isInitialized
}