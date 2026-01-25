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
