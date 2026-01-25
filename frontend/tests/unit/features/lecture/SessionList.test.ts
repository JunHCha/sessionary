import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import {
	savePendingSessionIdToStorage,
	getPendingSessionIdFromStorage,
	isUnauthorizedApiError
} from '$lib/features/lecture/components/SessionList.svelte'

describe('SessionList - Unauthenticated User Flow', () => {
	let mockSessionStorage: Record<string, string>

	beforeEach(() => {
		mockSessionStorage = {}

		vi.stubGlobal('sessionStorage', {
			getItem: vi.fn((key: string) => mockSessionStorage[key] || null),
			setItem: vi.fn((key: string, value: string) => {
				mockSessionStorage[key] = value
			}),
			removeItem: vi.fn((key: string) => {
				delete mockSessionStorage[key]
			}),
			clear: vi.fn(() => {
				mockSessionStorage = {}
			}),
			key: vi.fn(),
			length: 0
		} as Storage)
	})

	afterEach(() => {
		vi.unstubAllGlobals()
		vi.clearAllMocks()
	})

	describe('savePendingSessionIdToStorage', () => {
		it('세션 ID를 sessionStorage에 저장한다', () => {
			const sessionId = 123

			savePendingSessionIdToStorage(sessionId)

			expect(mockSessionStorage['pendingSessionId']).toBe('123')
		})

		it('여러 번 호출하면 마지막 값으로 덮어쓴다', () => {
			savePendingSessionIdToStorage(1)
			savePendingSessionIdToStorage(2)
			savePendingSessionIdToStorage(3)

			expect(mockSessionStorage['pendingSessionId']).toBe('3')
		})
	})

	describe('getPendingSessionIdFromStorage', () => {
		it('저장된 세션 ID를 가져온다', () => {
			mockSessionStorage['pendingSessionId'] = '456'

			const result = getPendingSessionIdFromStorage()

			expect(result).toBe(456)
		})

		it('세션 ID를 가져온 후 sessionStorage에서 제거한다', () => {
			mockSessionStorage['pendingSessionId'] = '789'

			getPendingSessionIdFromStorage()

			expect(mockSessionStorage['pendingSessionId']).toBeUndefined()
		})

		it('저장된 세션 ID가 없으면 null을 반환한다', () => {
			const result = getPendingSessionIdFromStorage()

			expect(result).toBeNull()
		})

		it('잘못된 형식의 세션 ID는 null로 반환한다', () => {
			mockSessionStorage['pendingSessionId'] = 'invalid'

			const result = getPendingSessionIdFromStorage()

			expect(result).toBeNull()
		})
	})

	describe('isUnauthorizedApiError', () => {
		it('401 상태 코드를 가진 에러는 true를 반환한다', () => {
			const error = { status: 401, message: 'Unauthorized' }

			const result = isUnauthorizedApiError(error)

			expect(result).toBe(true)
		})

		it('401이 아닌 상태 코드를 가진 에러는 false를 반환한다', () => {
			const error = { status: 403, message: 'Forbidden' }

			const result = isUnauthorizedApiError(error)

			expect(result).toBe(false)
		})

		it('status 속성이 없는 에러는 false를 반환한다', () => {
			const error = { message: 'Some error' }

			const result = isUnauthorizedApiError(error)

			expect(result).toBe(false)
		})

		it('null은 false를 반환한다', () => {
			const result = isUnauthorizedApiError(null)

			expect(result).toBe(false)
		})

		it('undefined는 false를 반환한다', () => {
			const result = isUnauthorizedApiError(undefined)

			expect(result).toBe(false)
		})

		it('문자열은 false를 반환한다', () => {
			const result = isUnauthorizedApiError('error')

			expect(result).toBe(false)
		})
	})
})
