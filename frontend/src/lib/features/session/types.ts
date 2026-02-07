import type {
	SessionDetailResponse,
	SessionType,
	Subtitle,
	PlayingGuideStep
} from '$lib/api/client/types.gen'

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

export type { SessionType, Subtitle, PlayingGuideStep }

export interface SessionDetailData {
	id: number
	title: string
	sessionType: SessionType
	sessionTypeLabel: string
	lectureOrdering: number
	lengthSec: number
	lectureId: number
	lectureTitle: string
	totalSessions: number
	videoUrl: string
	videoType: string
	sheetmusicUrl: string | null
	syncOffset: number
	subtitles: Array<Subtitle>
	playingGuide: Array<PlayingGuideStep>
	prevSessionId: number | null
	nextSessionId: number | null
}

export function toSessionDetailData(response: SessionDetailResponse): SessionDetailData {
	return {
		id: response.id,
		title: response.title,
		sessionType: response.session_type,
		sessionTypeLabel: response.session_type_label,
		lectureOrdering: response.lecture_ordering,
		lengthSec: response.length_sec,
		lectureId: response.lecture.id,
		lectureTitle: response.lecture.title,
		totalSessions: response.lecture.total_sessions,
		videoUrl: response.video?.url ?? '',
		videoType: response.video?.type ?? '',
		sheetmusicUrl: response.sheetmusic_url,
		syncOffset: response.sync_offset,
		subtitles: response.subtitles,
		playingGuide: response.playing_guide,
		prevSessionId: response.navigation.prev_session_id,
		nextSessionId: response.navigation.next_session_id
	}
}
