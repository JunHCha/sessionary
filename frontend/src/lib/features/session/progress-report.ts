/**
 * 시청 위치 리포팅 판정 (순수 함수 모듈, side-effect 없음)
 *
 * Svelte $effect 무한루프(effect_update_depth_exceeded, #125) 회귀 방지를 위해
 * 판정 로직을 순수함수로 분리한다. effect 안에서 같은 $state 를 쓰고-읽지 않도록
 * 다음 상태를 반환하면 호출부가 비반응 변수에 저장한다.
 */

const HEARTBEAT_INTERVAL_MS = 10_000
const THRESHOLD90 = 0.9

export interface ReportState {
	/** 마지막 report 시각(ms epoch) */
	lastReportedAt: number
	/** 90% 강제발화 1회성 플래그 */
	fired90: boolean
}

export interface PositionSample {
	currentTime: number
	duration: number
	now: number
}

export interface ReportDecision extends ReportState {
	shouldReport: boolean
	reason: 'heartbeat' | 'threshold90' | 'none'
}

export function createReportState(): ReportState {
	return { lastReportedAt: 0, fired90: false }
}

/**
 * 시청 비율(0~100 정수). duration 가드 포함.
 */
export function computePercent(positionSec: number, durationSec: number): number {
	if (durationSec <= 0) return 0
	const ratio = positionSec / durationSec
	return Math.min(100, Math.max(0, Math.round(ratio * 100)))
}

/**
 * 현재 위치 샘플로 리포팅 여부와 다음 상태를 계산한다.
 * - 90% 강제발화: duration>0 && currentTime >= duration*0.9 && !fired90 → throttle 무시 1회
 * - heartbeat: now - lastReportedAt >= 10초
 */
export function evaluatePositionReport(state: ReportState, sample: PositionSample): ReportDecision {
	const { currentTime, duration, now } = sample

	if (duration <= 0) {
		return { ...state, shouldReport: false, reason: 'none' }
	}

	const crossed90 = currentTime >= duration * THRESHOLD90
	if (crossed90 && !state.fired90) {
		return { lastReportedAt: now, fired90: true, shouldReport: true, reason: 'threshold90' }
	}

	if (now - state.lastReportedAt >= HEARTBEAT_INTERVAL_MS) {
		return {
			lastReportedAt: now,
			fired90: state.fired90,
			shouldReport: true,
			reason: 'heartbeat'
		}
	}

	return { ...state, shouldReport: false, reason: 'none' }
}
