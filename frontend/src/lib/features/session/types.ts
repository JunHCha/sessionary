/**
 * VideoPlayer 컴포넌트 Props
 */
export interface VideoPlayerProps {
	/** HLS URL (.m3u8) 또는 MP4 URL */
	src: string
	/** 썸네일 이미지 URL */
	poster?: string
	/** 자동 재생 여부 (기본: false) */
	autoplay?: boolean
}

/**
 * timeupdate 이벤트 데이터
 */
export interface TimeUpdateEvent {
	currentTime: number
	duration: number
}

/**
 * error 이벤트 데이터
 */
export interface ErrorEvent {
	message: string
}

/**
 * VideoPlayer Props 생성 (기본값 적용)
 */
export function createVideoPlayerProps(
	props: VideoPlayerProps
): Required<Pick<VideoPlayerProps, 'src' | 'autoplay'>> & Pick<VideoPlayerProps, 'poster'> {
	return {
		src: props.src,
		poster: props.poster,
		autoplay: props.autoplay ?? false
	}
}

/**
 * TimeUpdate 이벤트 객체 생성
 */
export function createTimeUpdateEvent(currentTime: number, duration: number): TimeUpdateEvent {
	return { currentTime, duration }
}

/**
 * Error 이벤트 객체 생성
 */
export function createErrorEvent(message: string): ErrorEvent {
	return { message }
}
