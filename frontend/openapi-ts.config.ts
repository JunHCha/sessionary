import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
	// 라이브 백엔드 대신 커밋된 스펙 스냅샷을 단일 진실 소스로 사용한다.
	// 백엔드 응답 계약이 바뀌면 `backend/openapi.json` 을 재생성·커밋해야 하고,
	// 그래야 client 타입이 따라 갱신된다. (CI 가 양쪽 drift 를 검증)
	input: '../backend/openapi.json',
	output: './src/lib/api/client',
	client: 'axios'
})
