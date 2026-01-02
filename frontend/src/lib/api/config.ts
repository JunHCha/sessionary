import { OpenAPI } from './client'

let isInitialized = false
let resolveInit: (() => void) | null = null
const initPromise = new Promise<void>((resolve) => {
	resolveInit = resolve
})

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

export function waitForApiInit(): Promise<void> {
	if (isInitialized) return Promise.resolve()
	return initPromise
}

export function isApiInitialized(): boolean {
	return isInitialized
}
