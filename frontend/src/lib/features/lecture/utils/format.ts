/**
 * 초 단위 지속 시간을 "분:초" 형식의 문자열로 변환한다.
 *
 * @param seconds - 변환할 전체 초 수
 * @returns `분:초` 형식의 문자열, 초는 두 자리로 왼쪽을 0으로 채움 (예: `3:05`)
 */
export function formatDuration(seconds: number): string {
	const minutes = Math.floor(seconds / 60)
	const remainingSeconds = seconds % 60
	return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

/**
 * 썸네일 경로를 결정하여 반환합니다.
 *
 * @param thumbnail - 사용할 썸네일 경로. 값이 없거나 `null`이면 `defaultThumbnail`이 사용됩니다.
 * @param defaultThumbnail - `thumbnail`이 없을 때 대체로 사용할 기본 썸네일 경로
 * @returns 사용 가능한 썸네일 경로(제공된 `thumbnail` 또는 `defaultThumbnail`)
 */
export function getThumbnailSrc(
	thumbnail: string | null,
	defaultThumbnail = '/thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png'
): string {
	return thumbnail || defaultThumbnail
}