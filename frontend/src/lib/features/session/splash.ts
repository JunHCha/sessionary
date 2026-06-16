/**
 * 세션 로딩 스플래시 최소 표시 시간 (ms).
 * 스플래시 진입 시각 기준으로 이 시간만큼은 무조건 노출한다.
 */
export const MIN_SPLASH_MS = 2000

/**
 * 영상 프리로드 타임아웃 상한 (ms).
 * 프리로드가 실패/지연되어도 이 시간이 지나면 영상 항목을 ready로 간주해
 * (최소 시간 조건만 충족되면) 전환을 막지 않는다.
 */
export const PRELOAD_TIMEOUT_MS = 8000

/**
 * 스플래시에서 본 화면으로 전환할지 판정.
 * 최소 표시 시간 경과 && 리소스 준비 완료, 두 조건 모두 충족 시에만 true.
 */
export function shouldTransitionFromSplash(input: {
	minElapsed: boolean
	resourcesReady: boolean
}): boolean {
	return input.minElapsed && input.resourcesReady
}

/**
 * 영상/자막/악보 항목별 준비 여부를 모아 전체 준비 판정.
 */
export function areResourcesReady(input: {
	video: boolean
	subtitles: boolean
	sheet: boolean
}): boolean {
	return input.video && input.subtitles && input.sheet
}

/**
 * 악보 준비 여부.
 * URL이 null이면 해당 항목 자체가 없으므로 즉시 ready.
 */
export function isSheetReady(sheetmusicUrl: string | null, loaded: boolean): boolean {
	if (sheetmusicUrl === null) return true
	return loaded
}

/**
 * 영상 준비 여부.
 * videoUrl이 빈 문자열이면 영상 없는 세션이므로 즉시 ready.
 * 그 외에는 프리로드 완료 신호가 필요.
 */
export function isVideoReady(videoUrl: string, preloaded: boolean): boolean {
	if (videoUrl === '') return true
	return preloaded
}

/**
 * 영상 프리로드 이벤트를 ready 신호로 볼지 판정.
 * - MP4: loadedmetadata / canplay
 * - HLS(hls.js): manifestparsed
 */
export function videoPreloadEventToReady(eventType: string): boolean {
	return (
		eventType === 'loadedmetadata' || eventType === 'canplay' || eventType === 'manifestparsed'
	)
}
