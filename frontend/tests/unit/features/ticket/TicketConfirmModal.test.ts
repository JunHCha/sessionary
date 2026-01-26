import { describe, it, expect } from 'vitest'

describe('TicketConfirmModal', () => {
	describe('Props 기본값', () => {
		it('getConfirmMessage 함수는 티켓 사용 안내 문구를 반환한다', async () => {
			const { getConfirmMessage } = await import(
				'$lib/features/ticket/components/TicketConfirmModal.svelte'
			)
			expect(getConfirmMessage()).toBe('티켓 1개를 사용하여 이 강의에 접근합니다')
		})

		it('getAccessPeriodMessage 함수는 시청 가능 기간 안내를 반환한다', async () => {
			const { getAccessPeriodMessage } = await import(
				'$lib/features/ticket/components/TicketConfirmModal.svelte'
			)
			expect(getAccessPeriodMessage()).toBe('1주간 무제한 시청 가능')
		})

		it('formatTicketCount 함수는 보유 티켓 수를 포맷팅한다', async () => {
			const { formatTicketCount } = await import(
				'$lib/features/ticket/components/TicketConfirmModal.svelte'
			)
			expect(formatTicketCount(5)).toBe('현재 보유 티켓 수: 5개')
			expect(formatTicketCount(0)).toBe('현재 보유 티켓 수: 0개')
		})
	})
})
