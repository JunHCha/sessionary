<script lang="ts" module>
	/**
	 * 남은 시간을 1초 감소시킨다 (0 미만 방지)
	 */
	export function tickCountdown(remaining: number): number {
		return Math.max(0, remaining - 1)
	}

	/**
	 * 카운트다운 만료 여부 (0 이하)
	 */
	export function isExpired(remaining: number): boolean {
		return remaining <= 0
	}

	/**
	 * 남은 초를 표시 문자열로 변환
	 */
	export function formatCountdown(remaining: number): string {
		return String(Math.max(0, Math.ceil(remaining)))
	}

	/**
	 * 원형 진행률 링의 stroke-dashoffset 계산
	 * remaining이 total일 때 0(가득 참), 0일 때 circumference(비어 있음)
	 */
	export function progressOffset(
		remaining: number,
		total: number,
		circumference: number
	): number {
		if (total <= 0) return 0
		const ratio = Math.min(1, Math.max(0, remaining / total))
		return circumference * (1 - ratio)
	}
</script>

<script lang="ts">
	const RADIUS = 36
	const CIRCUMFERENCE = 2 * Math.PI * RADIUS

	let {
		nextSessionId,
		nextSessionTitle,
		nextOrdering,
		seconds = 5,
		onstart,
		oncancel
	}: {
		nextSessionId: number
		nextSessionTitle: string | null
		nextOrdering: number
		seconds?: number
		onstart: () => void
		oncancel: () => void
	} = $props()

	// svelte-ignore state_referenced_locally
	let remaining = $state(seconds)

	const offset = $derived(progressOffset(remaining, seconds, CIRCUMFERENCE))

	$effect(() => {
		const interval = setInterval(() => {
			remaining = tickCountdown(remaining)
			if (isExpired(remaining)) {
				clearInterval(interval)
				onstart()
			}
		}, 1000)

		return () => clearInterval(interval)
	})
</script>

<div
	class="absolute inset-0 z-20 flex items-center justify-center bg-black/70"
	data-testid="next-session-countdown"
	data-next-session-id={nextSessionId}
>
	<div class="mx-4 flex w-full max-w-sm flex-col items-center gap-4 rounded-2xl bg-zinc-900/95 p-6 text-center shadow-xl">
		<p class="text-sm text-zinc-400">다음 세션 {nextOrdering}</p>
		<p class="text-lg font-semibold text-white">{nextSessionTitle ?? '다음 세션'}</p>

		<div class="relative flex h-24 w-24 items-center justify-center">
			<svg class="h-24 w-24 -rotate-90" viewBox="0 0 80 80">
				<circle cx="40" cy="40" r={RADIUS} fill="none" stroke="#3f3f46" stroke-width="6" />
				<circle
					cx="40"
					cy="40"
					r={RADIUS}
					fill="none"
					stroke="#FF5C16"
					stroke-width="6"
					stroke-linecap="round"
					stroke-dasharray={CIRCUMFERENCE}
					stroke-dashoffset={offset}
				/>
			</svg>
			<span
				class="absolute text-2xl font-bold text-white"
				data-testid="countdown-seconds">{formatCountdown(remaining)}</span
			>
		</div>

		<p class="text-xs text-zinc-400">{formatCountdown(remaining)}초 후 자동 이동</p>

		<div class="flex w-full gap-2">
			<button
				type="button"
				class="flex-1 rounded-lg border border-zinc-600 px-4 py-2 text-sm font-medium text-zinc-300 transition hover:bg-zinc-800"
				data-testid="countdown-cancel-btn"
				onclick={oncancel}>취소</button
			>
			<button
				type="button"
				class="flex-1 rounded-lg bg-[#FF5C16] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#FF5C16]/90"
				data-testid="countdown-start-btn"
				onclick={onstart}>지금 시작</button
			>
		</div>
	</div>
</div>
