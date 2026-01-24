import { describe, it, expect } from 'vitest'

describe('TicketInsufficientModal', () => {
	describe('Props 기본값', () => {
		it('getInsufficientTitle 함수는 티켓 부족 제목을 반환한다', async () => {
			const { getInsufficientTitle } = await import(
				'$lib/features/ticket/components/TicketInsufficientModal.svelte'
			)
			expect(getInsufficientTitle()).toBe('티켓이 부족합니다')
		})

		it('getRefillMessage 함수는 충전 안내 문구를 반환한다', async () => {
			const { getRefillMessage } = await import(
				'$lib/features/ticket/components/TicketInsufficientModal.svelte'
			)
			expect(getRefillMessage()).toBe('티켓은 매주 충전됩니다')
		})

		it('formatDaysUntilRefill 함수는 남은 일수를 포맷팅한다', async () => {
			const { formatDaysUntilRefill } = await import(
				'$lib/features/ticket/components/TicketInsufficientModal.svelte'
			)
			expect(formatDaysUntilRefill(3)).toBe('다음 충전까지 3일 남았습니다')
			expect(formatDaysUntilRefill(1)).toBe('다음 충전까지 1일 남았습니다')
		})
	})
})
