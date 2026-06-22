import { describe, it, expect } from 'vitest'
import {
	evaluatePositionReport,
	createReportState,
	computePercent,
	buildPositionBeacon,
	type ReportState
} from '$lib/features/session/progress-report'

const state = (overrides: Partial<ReportState> = {}): ReportState => ({
	lastReportedAt: 0,
	fired90: false,
	...overrides
})

describe('computePercent', () => {
	it('position/duration 비율을 0~100 정수로 반환', () => {
		expect(computePercent(45, 90)).toBe(50)
		expect(computePercent(90, 90)).toBe(100)
	})

	it('duration이 0 이하이면 0', () => {
		expect(computePercent(10, 0)).toBe(0)
		expect(computePercent(10, -5)).toBe(0)
	})

	it('100을 넘지 않도록 클램프', () => {
		expect(computePercent(120, 100)).toBe(100)
	})
})

describe('evaluatePositionReport - heartbeat', () => {
	it('10초가 지나지 않으면(9.9s) report 안 함', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 0 }), {
			currentTime: 1,
			duration: 600,
			now: 9_900
		})
		expect(result.shouldReport).toBe(false)
		expect(result.lastReportedAt).toBe(0)
		expect(result.fired90).toBe(false)
	})

	it('정확히 10초 경과 시 heartbeat report', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 0 }), {
			currentTime: 1,
			duration: 600,
			now: 10_000
		})
		expect(result.shouldReport).toBe(true)
		expect(result.reason).toBe('heartbeat')
		expect(result.lastReportedAt).toBe(10_000)
	})
})

describe('evaluatePositionReport - 90% 강제발화', () => {
	it('90% 지점을 처음 통과하면 throttle 무시하고 report', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 9_500, fired90: false }), {
			currentTime: 540,
			duration: 600,
			now: 9_600
		})
		expect(result.shouldReport).toBe(true)
		expect(result.reason).toBe('threshold90')
		expect(result.fired90).toBe(true)
		expect(result.lastReportedAt).toBe(9_600)
	})

	it('이미 fired90 이면 90% 이상이어도 강제발화 안 함(1회성)', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 9_500, fired90: true }), {
			currentTime: 590,
			duration: 600,
			now: 9_600
		})
		expect(result.shouldReport).toBe(false)
		expect(result.fired90).toBe(true)
	})

	it('짧은 영상(15s)도 heartbeat 없이 90%에서 강제발화', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 0, fired90: false }), {
			currentTime: 13.5,
			duration: 15,
			now: 2_000
		})
		expect(result.shouldReport).toBe(true)
		expect(result.reason).toBe('threshold90')
		expect(result.fired90).toBe(true)
	})
})

describe('evaluatePositionReport - duration 가드', () => {
	it('duration이 0이면 report 안 함', () => {
		const result = evaluatePositionReport(state({ lastReportedAt: 0 }), {
			currentTime: 5,
			duration: 0,
			now: 20_000
		})
		expect(result.shouldReport).toBe(false)
		expect(result.fired90).toBe(false)
	})
})

describe('buildPositionBeacon', () => {
	it('PUT position URL과 JSON Blob payload를 만든다', () => {
		const beacon = buildPositionBeacon('https://api.test', 700, 45.6, 90.2)
		expect(beacon.url).toBe('https://api.test/progress/lesson/700/position')
		expect(beacon.blob.type).toBe('application/json')
	})

	it('position/duration을 정수로 반올림한다', async () => {
		const beacon = buildPositionBeacon('https://api.test', 700, 45.6, 90.2)
		const body = JSON.parse(await beacon.blob.text())
		expect(body).toEqual({ position_sec: 46, duration_sec: 90 })
	})

	it('baseUrl 끝 슬래시를 정규화한다', () => {
		const beacon = buildPositionBeacon('https://api.test/', 700, 0, 0)
		expect(beacon.url).toBe('https://api.test/progress/lesson/700/position')
	})
})

describe('createReportState', () => {
	it('초기 상태는 lastReportedAt=0, fired90=false', () => {
		expect(createReportState()).toEqual({ lastReportedAt: 0, fired90: false })
	})
})
