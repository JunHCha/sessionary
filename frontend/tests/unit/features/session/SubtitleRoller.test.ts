import { describe, it, expect } from 'vitest'

describe('SubtitleRoller', () => {
	describe('computeLineStyle', () => {
		it('정면(offset=0)은 변형이 없고 불투명도 1, 활성 상태다', async () => {
			const { computeLineStyle } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			const style = computeLineStyle(0)

			expect(style.transform).toBe('translateY(0)')
			expect(style.transformOrigin).toBe('center center')
			expect(style.opacity).toBe(1)
			expect(style.isActive).toBe(true)
		})

		it('위쪽(offset<0)은 하단을 축으로 양의 rotateX를 적용한다', async () => {
			const { computeLineStyle } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			const style = computeLineStyle(-1)

			expect(style.transformOrigin).toBe('center bottom')
			expect(style.transform).toBe('translateY(-30px) rotateX(54deg)')
			expect(style.opacity).toBe(0.3)
			expect(style.isActive).toBe(false)
		})

		it('아래쪽(offset>0)은 상단을 축으로 음의 rotateX를 적용한다', async () => {
			const { computeLineStyle } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			const style = computeLineStyle(1)

			expect(style.transformOrigin).toBe('center top')
			expect(style.transform).toBe('translateY(30px) rotateX(-54deg)')
			expect(style.opacity).toBe(0.3)
		})

		it('거리 2는 불투명도 0.08, 거리 3 이상은 0이다', async () => {
			const { computeLineStyle } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			expect(computeLineStyle(2).opacity).toBe(0.08)
			expect(computeLineStyle(-2).opacity).toBe(0.08)
			expect(computeLineStyle(3).opacity).toBe(0)
			expect(computeLineStyle(-4).opacity).toBe(0)
		})
	})

	describe('computeWheelIndex', () => {
		it('deltaY>0이면 다음 인덱스로 이동한다', async () => {
			const { computeWheelIndex } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			expect(computeWheelIndex(2, 10, 7)).toBe(3)
		})

		it('deltaY<0이면 이전 인덱스로 이동한다', async () => {
			const { computeWheelIndex } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			expect(computeWheelIndex(2, -10, 7)).toBe(1)
		})

		it('범위를 벗어나지 않게 클램프한다', async () => {
			const { computeWheelIndex } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			expect(computeWheelIndex(0, -10, 7)).toBe(0)
			expect(computeWheelIndex(6, 10, 7)).toBe(6)
		})
	})

	describe('resolveActiveIndex', () => {
		it('manualIndex가 null이면 재생 시간 기준 활성 인덱스를 사용한다', async () => {
			const { resolveActiveIndex } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			const subtitles = [
				{ timestamp_ms: 0, text: 'a' },
				{ timestamp_ms: 5000, text: 'b' },
				{ timestamp_ms: 10000, text: 'c' }
			]
			expect(resolveActiveIndex(null, subtitles, 6000)).toBe(1)
		})

		it('manualIndex가 있으면 그 값을 우선한다', async () => {
			const { resolveActiveIndex } =
				await import('$lib/features/session/components/SubtitleRoller.svelte')
			const subtitles = [
				{ timestamp_ms: 0, text: 'a' },
				{ timestamp_ms: 5000, text: 'b' },
				{ timestamp_ms: 10000, text: 'c' }
			]
			expect(resolveActiveIndex(2, subtitles, 6000)).toBe(2)
		})
	})
})
