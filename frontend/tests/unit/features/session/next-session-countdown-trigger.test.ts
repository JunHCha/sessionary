import { describe, it, expect } from 'vitest'

describe('shouldShowCountdown', () => {
	it('다음 세션이 있으면 true를 반환한다', async () => {
		const { shouldShowCountdown } = await import('$lib/features/session/utils')
		expect(shouldShowCountdown(43)).toBe(true)
	})

	it('다음 세션이 없으면(null) false를 반환한다', async () => {
		const { shouldShowCountdown } = await import('$lib/features/session/utils')
		expect(shouldShowCountdown(null)).toBe(false)
	})

	it('다음 세션이 undefined이면 false를 반환한다', async () => {
		const { shouldShowCountdown } = await import('$lib/features/session/utils')
		expect(shouldShowCountdown(undefined)).toBe(false)
	})
})
