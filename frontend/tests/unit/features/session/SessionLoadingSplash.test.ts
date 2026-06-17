import { describe, it, expect } from 'vitest'

describe('SessionLoadingSplash', () => {
	describe('getDefaultProps', () => {
		it('label 기본값은 빈 문자열이다', async () => {
			const { getDefaultProps } =
				await import('$lib/features/session/components/SessionLoadingSplash.svelte')
			expect(getDefaultProps().label).toBe('')
		})
	})

	describe('SPLASH_TESTID', () => {
		it('스플래시 testid 상수를 제공한다', async () => {
			const { SPLASH_TESTID } =
				await import('$lib/features/session/components/SessionLoadingSplash.svelte')
			expect(SPLASH_TESTID).toBe('session-loading-splash')
		})
	})
})
