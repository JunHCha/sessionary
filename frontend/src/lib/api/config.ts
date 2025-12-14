import { OpenAPI } from './client'

export function initializeApi(baseUrl: string) {
	OpenAPI.BASE = baseUrl
	OpenAPI.WITH_CREDENTIALS = true
	OpenAPI.interceptors.request.use((request) => {
		request.withCredentials = true
		return request
	})
}
