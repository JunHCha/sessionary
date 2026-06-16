/**
 * 재생 속도 옵션 (오름차순)
 */
export const PLAYBACK_SPEEDS = [0.5, 0.75, 1.0, 1.25, 1.5] as const

/**
 * 초 단위 시간을 "분:초" 형식으로 포맷
 * @param seconds 초 단위 시간
 * @returns "분:초" 형식 문자열 (예: "2:05")
 */
export function formatTime(seconds: number): string {
	if (isNaN(seconds) || seconds < 0) {
		return '0:00'
	}

	const mins = Math.floor(seconds / 60)
	const secs = Math.floor(seconds % 60)
	return `${mins}:${secs.toString().padStart(2, '0')}`
}

/**
 * URL이 HLS 소스(.m3u8)인지 확인
 * @param src 비디오 소스 URL
 * @returns HLS 소스 여부
 */
export function isHlsSource(src: string): boolean {
	const url = src.split('?')[0]
	return url.toLowerCase().endsWith('.m3u8')
}

/**
 * 영상 종료 시 다음 세션 카운트다운 오버레이를 표시할지 판단.
 * 다음 세션이 있을 때만 표시한다(마지막 세션 예외).
 */
export function shouldShowCountdown(nextSessionId: number | null | undefined): boolean {
	return nextSessionId != null
}

export function parseSessionId(raw: string): number {
	const id = Number(raw)
	if (isNaN(id) || !Number.isInteger(id) || id <= 0) {
		throw new Error('Invalid session ID')
	}
	return id
}

import type { Subtitle } from '$lib/api/client/types.gen'

/**
 * 현재 시간(ms)에 해당하는 활성 자막 인덱스를 반환.
 * 자막이 없거나 첫 자막 이전이면 -1.
 *
 * @precondition subtitles는 timestamp_ms 기준 오름차순 정렬이어야 함
 */
export function findActiveSubtitleIndex(subtitles: Array<Subtitle>, currentTimeMs: number): number {
	if (subtitles.length === 0) return -1
	let activeIndex = -1
	for (let i = 0; i < subtitles.length; i++) {
		if (subtitles[i].timestamp_ms <= currentTimeMs) {
			activeIndex = i
		} else {
			break
		}
	}
	return activeIndex
}

/**
 * timestamp_ms를 "분:초" 형식으로 변환
 */
export function formatSubtitleTimestamp(timestampMs: number): string {
	return formatTime(timestampMs / 1000)
}
