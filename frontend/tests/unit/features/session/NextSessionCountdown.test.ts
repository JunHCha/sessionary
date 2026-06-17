import { describe, it, expect } from 'vitest'

describe('NextSessionCountdown', () => {
	describe('tickCountdown', () => {
		it('남은 시간을 1 감소시킨다', async () => {
			const { tickCountdown } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(tickCountdown(5)).toBe(4)
			expect(tickCountdown(1)).toBe(0)
		})

		it('0 미만으로 내려가지 않는다', async () => {
			const { tickCountdown } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(tickCountdown(0)).toBe(0)
		})
	})

	describe('isExpired', () => {
		it('0 이하이면 만료로 판단한다', async () => {
			const { isExpired } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(isExpired(0)).toBe(true)
			expect(isExpired(-1)).toBe(true)
		})

		it('0보다 크면 만료가 아니다', async () => {
			const { isExpired } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(isExpired(1)).toBe(false)
			expect(isExpired(5)).toBe(false)
		})
	})

	describe('formatCountdown', () => {
		it('남은 초를 문자열로 표시한다', async () => {
			const { formatCountdown } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(formatCountdown(5)).toBe('5')
			expect(formatCountdown(0)).toBe('0')
		})
	})

	describe('progressOffset', () => {
		it('남은 시간 비율에 따른 stroke dashoffset을 계산한다 (full circle)', async () => {
			const { progressOffset } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			const circumference = 100
			// 전체 시간일 때 offset 0 (링 가득 참)
			expect(progressOffset(5, 5, circumference)).toBe(0)
			// 절반 남았을 때 offset은 둘레의 절반
			expect(progressOffset(2.5, 5, circumference)).toBeCloseTo(50)
			// 0초 남았을 때 offset은 둘레 전체 (링 비어있음)
			expect(progressOffset(0, 5, circumference)).toBe(circumference)
		})

		it('total이 0이면 offset 0을 반환한다 (0 나눗셈 방지)', async () => {
			const { progressOffset } = await import(
				'$lib/features/session/components/NextSessionCountdown.svelte'
			)
			expect(progressOffset(0, 0, 100)).toBe(0)
		})
	})
})
