import { describe, it, expect } from 'vitest'

describe('Video Player Types', () => {
	describe('createVideoPlayerProps', () => {
		it('src만 제공하면 기본값이 적용된 props를 반환한다', async () => {
			const { createVideoPlayerProps } = await import('$lib/features/session/types')
			const props = createVideoPlayerProps({ src: 'https://example.com/video.m3u8' })

			expect(props.src).toBe('https://example.com/video.m3u8')
			expect(props.poster).toBeUndefined()
			expect(props.autoplay).toBe(false)
		})

		it('모든 옵션을 제공하면 해당 값이 적용된다', async () => {
			const { createVideoPlayerProps } = await import('$lib/features/session/types')
			const props = createVideoPlayerProps({
				src: 'https://example.com/video.m3u8',
				poster: 'https://example.com/thumb.jpg',
				autoplay: true
			})

			expect(props.src).toBe('https://example.com/video.m3u8')
			expect(props.poster).toBe('https://example.com/thumb.jpg')
			expect(props.autoplay).toBe(true)
		})
	})

	describe('createTimeUpdateEvent', () => {
		it('currentTime과 duration으로 이벤트 객체를 생성한다', async () => {
			const { createTimeUpdateEvent } = await import('$lib/features/session/types')
			const event = createTimeUpdateEvent(30.5, 120)

			expect(event.currentTime).toBe(30.5)
			expect(event.duration).toBe(120)
		})
	})

	describe('createErrorEvent', () => {
		it('에러 메시지로 이벤트 객체를 생성한다', async () => {
			const { createErrorEvent } = await import('$lib/features/session/types')
			const event = createErrorEvent('Failed to load video')

			expect(event.message).toBe('Failed to load video')
		})
	})
})
