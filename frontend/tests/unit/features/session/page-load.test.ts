import { describe, it, expect } from 'vitest'

describe('Session [id] Page Load - parseSessionId', () => {
	it('유효한 숫자 문자열을 파싱하여 sessionId를 반환한다', async () => {
		const { parseSessionId } = await import('$lib/features/session/utils')
		expect(parseSessionId('42')).toBe(42)
	})

	it('숫자가 아닌 문자열은 에러를 throw한다', async () => {
		const { parseSessionId } = await import('$lib/features/session/utils')
		expect(() => parseSessionId('abc')).toThrow('Invalid session ID')
	})

	it('0은 에러를 throw한다', async () => {
		const { parseSessionId } = await import('$lib/features/session/utils')
		expect(() => parseSessionId('0')).toThrow('Invalid session ID')
	})

	it('음수는 에러를 throw한다', async () => {
		const { parseSessionId } = await import('$lib/features/session/utils')
		expect(() => parseSessionId('-1')).toThrow('Invalid session ID')
	})

	it('소수점이 포함된 문자열은 에러를 throw한다', async () => {
		const { parseSessionId } = await import('$lib/features/session/utils')
		expect(() => parseSessionId('1.5')).toThrow('Invalid session ID')
	})
})
