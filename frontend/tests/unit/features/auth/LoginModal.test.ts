import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

// Mock sessionStorage
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

describe('LoginModal', () => {
	describe('Props 기본값', () => {
		it('message 기본값은 "로그인이 필요합니다"이다', async () => {
			// LoginModal 컴포넌트의 기본 message prop 확인
			const { getDefaultMessage } = await import('$lib/features/auth/components/LoginModal.svelte')
			expect(getDefaultMessage()).toBe('로그인이 필요합니다')
		})

		it('redirectUrl 기본값은 "/home"이다', async () => {
			// LoginModal 컴포넌트의 기본 redirectUrl prop 확인
			const { getDefaultRedirectUrl } = await import('$lib/features/auth/components/LoginModal.svelte')
			expect(getDefaultRedirectUrl()).toBe('/home')
		})
	})

	describe('sessionStorage 저장', () => {
		it('saveRedirectUrl 호출 시 sessionStorage에 redirectUrl이 저장된다', async () => {
			const { saveRedirectUrl } = await import('$lib/features/auth/components/LoginModal.svelte')
			saveRedirectUrl('/my-page')
			expect(mockSessionStorage.setItem).toHaveBeenCalledWith('redirectUrl', '/my-page')
		})

		it('getDefaultRedirectUrl()로 기본값 "/home"을 가져올 수 있다', async () => {
			const { saveRedirectUrl, getDefaultRedirectUrl } = await import('$lib/features/auth/components/LoginModal.svelte')
			saveRedirectUrl(getDefaultRedirectUrl())
			expect(mockSessionStorage.setItem).toHaveBeenCalledWith('redirectUrl', '/home')
		})
	})
})
