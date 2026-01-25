import { describe, it, expect } from 'vitest'

describe('VideoControls', () => {
	describe('getNextPlaybackSpeed', () => {
		it('현재 속도 다음 속도를 반환한다', async () => {
			const { getNextPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(getNextPlaybackSpeed(1.0)).toBe(1.25)
		})

		it('마지막 속도에서는 첫 번째 속도로 순환한다', async () => {
			const { getNextPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(getNextPlaybackSpeed(1.5)).toBe(0.5)
		})

		it('목록에 없는 속도는 기본 1.0을 반환한다', async () => {
			const { getNextPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(getNextPlaybackSpeed(2.0)).toBe(1.0)
		})
	})

	describe('formatPlaybackSpeed', () => {
		it('1.0 속도를 "1x"로 포맷한다', async () => {
			const { formatPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(formatPlaybackSpeed(1.0)).toBe('1x')
		})

		it('0.5 속도를 "0.5x"로 포맷한다', async () => {
			const { formatPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(formatPlaybackSpeed(0.5)).toBe('0.5x')
		})

		it('1.25 속도를 "1.25x"로 포맷한다', async () => {
			const { formatPlaybackSpeed } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(formatPlaybackSpeed(1.25)).toBe('1.25x')
		})
	})

	describe('calculateProgress', () => {
		it('현재 시간과 총 시간으로 진행률(%)을 계산한다', async () => {
			const { calculateProgress } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(calculateProgress(30, 120)).toBe(25)
		})

		it('총 시간이 0이면 0을 반환한다', async () => {
			const { calculateProgress } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(calculateProgress(30, 0)).toBe(0)
		})

		it('총 시간이 NaN이면 0을 반환한다', async () => {
			const { calculateProgress } = await import(
				'$lib/features/session/components/VideoControls.svelte'
			)
			expect(calculateProgress(30, NaN)).toBe(0)
		})
	})
})
