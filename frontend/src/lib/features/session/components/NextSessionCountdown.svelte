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
	const RADIUS = 44
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

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
	data-testid="next-session-countdown"
	data-next-session-id={nextSessionId}
	onclick={oncancel}
>
	<div class="relative flex items-center justify-center">
		<!-- 원형 카운트다운 링 -->
		<svg
			class="-rotate-90"
			width="120"
			height="120"
			viewBox="0 0 100 100"
		>
			<!-- 배경 트랙 -->
			<circle
				cx="50"
				cy="50"
				r={RADIUS}
				fill="none"
				stroke="#3f3f46"
				stroke-width="5"
			/>
			<!-- 진행 링 -->
			<circle
				cx="50"
				cy="50"
				r={RADIUS}
				fill="none"
				stroke="#FF5C16"
				stroke-width="5"
				stroke-linecap="round"
				stroke-dasharray={CIRCUMFERENCE}
				stroke-dashoffset={offset}
				style="transition: stroke-dashoffset 1s linear;"
			/>
		</svg>

		<!-- 중앙 next 버튼 -->
		<button
			type="button"
			class="absolute flex h-[100px] w-[100px] items-center justify-center rounded-full bg-[#FF5C16] shadow-lg transition-transform hover:scale-105 active:scale-95"
			data-testid="countdown-start-btn"
			aria-label="다음 세션으로 이동: {nextSessionTitle ?? '다음 세션'}"
			onclick={(e) => { e.stopPropagation(); onstart(); }}
		>
			<svg
				width="40"
				height="40"
				viewBox="0 0 24 24"
				fill="white"
				aria-hidden="true"
			>
				<path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" />
			</svg>
		</button>
	</div>
</div>
