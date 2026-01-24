import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

const mockSessionStorage = {
	store: {} as Record<string, string>,
	getItem: vi.fn((key: string) => mockSessionStorage.store[key] || null),
	setItem: vi.fn((key: string, value: string) => {
		mockSessionStorage.store[key] = value
	}),
	removeItem: vi.fn((key: string) => {
		delete mockSessionStorage.store[key]
	}),
	clear: vi.fn(() => {
		mockSessionStorage.store = {}
	})
}

beforeEach(() => {
	mockSessionStorage.clear()
	vi.clearAllMocks()
	vi.stubGlobal('sessionStorage', mockSessionStorage)
})

afterEach(() => {
	vi.unstubAllGlobals()
})

describe('pendingAction', () => {
	describe('savePendingAction', () => {
		it('sessionStorage에 pendingAction을 JSON으로 저장한다', async () => {
			const { savePendingAction } = await import('$lib/features/auth/utils/pendingAction')
			const action = { type: 'access-session', sessionId: 1 }

			savePendingAction(action)

			expect(mockSessionStorage.setItem).toHaveBeenCalledWith(
				'pendingAction',
				JSON.stringify(action)
			)
		})
	})

	describe('getPendingAction', () => {
		it('저장된 pendingAction을 반환하고 삭제한다', async () => {
			const { savePendingAction, getPendingAction } = await import(
				'$lib/features/auth/utils/pendingAction'
			)
			const action = { type: 'access-session', sessionId: 1 }
			savePendingAction(action)

			const result = getPendingAction()

			expect(result).toEqual(action)
			expect(mockSessionStorage.removeItem).toHaveBeenCalledWith('pendingAction')
		})

		it('pendingAction이 없으면 null을 반환한다', async () => {
			const { getPendingAction } = await import('$lib/features/auth/utils/pendingAction')

			const result = getPendingAction()

			expect(result).toBeNull()
		})
	})
})
