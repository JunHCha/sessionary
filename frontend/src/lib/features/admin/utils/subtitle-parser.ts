export interface SubtitleRow {
	timestamp_ms: number
	text: string
}

function toMs(stamp: string): number {
	const m = stamp.trim().match(/(\d{2}):(\d{2}):(\d{2})[.,](\d{3})/)
	if (!m) return 0
	const [, h, min, s, ms] = m
	return ((+h * 60 + +min) * 60 + +s) * 1000 + +ms
}

export function parseSubtitles(input: string): SubtitleRow[] {
	const text = input.replace(/^WEBVTT.*$/m, '').trim()
	if (!text) return []
	const blocks = text.split(/\n\s*\n/)
	const rows: SubtitleRow[] = []
	for (const block of blocks) {
		const lines = block
			.split('\n')
			.map((l) => l.trim())
			.filter(Boolean)
		const cueIndex = lines.findIndex((l) => l.includes('-->'))
		if (cueIndex === -1) continue
		const start = lines[cueIndex].split('-->')[0]
		const body = lines
			.slice(cueIndex + 1)
			.join(' ')
			.trim()
		if (!body) continue
		rows.push({ timestamp_ms: toMs(start), text: body })
	}
	return rows
}
