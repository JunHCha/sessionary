<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import type { SessionState } from '../utils/progress'
	import { formatDuration } from '../utils/format'

	let {
		session,
		index,
		state = 'locked',
		onclick
	}: {
		session: LessonInLecture
		index: number
		state?: SessionState
		onclick?: () => void
	} = $props()

	let displayNumber = $derived(String(index + 1).padStart(2, '0'))

	let isCurrent = $derived(state === 'current')
	let isCompleted = $derived(state === 'completed')
	let numberColor = $derived(isCurrent ? '#ff5c16' : isCompleted ? '#3a3a3a' : '#656565')
</script>

<button
	type="button"
	data-testid="session-item"
	data-state={state}
	class="flex w-full items-center gap-[18px] rounded-[8px] border px-[20px] py-[16px] text-left transition-colors duration-150"
	class:current={isCurrent}
	style={isCurrent
		? 'border-color: #ff5c16; background: linear-gradient(to right, #1d1410, #0e0b09); box-shadow: 0 10px 30px -12px rgba(255,92,22,0.35);'
		: 'border-color: #242424; background: #141414;'}
	{onclick}
>
	<span
		class="min-w-[30px] text-[18px] font-bold"
		style="color: {numberColor}; font-family: Helvetica, Arial, sans-serif;"
	>
		{displayNumber}
	</span>

	<div class="min-w-0 flex-1">
		<p
			class="truncate text-[15px] font-semibold"
			style="color: {isCurrent ? '#ffffff' : isCompleted ? '#656565' : '#c9c9c9'};"
		>
			{session.title}
		</p>
	</div>

	<div class="flex flex-shrink-0 items-center gap-[14px]">
		<span class="text-[13px]" style="color: {isCurrent ? '#c9c9c9' : '#848484'};">
			{formatDuration(session.length_sec)}
		</span>

		{#if isCurrent}
			<span
				class="rounded-full px-[9px] py-[3px] text-[10px] font-bold text-white"
				style="background: #ff5c16; font-family: Helvetica, Arial, sans-serif;"
			>
				NEXT
			</span>
		{:else if isCompleted}
			<span
				class="flex h-[22px] w-[22px] items-center justify-center rounded-full"
				style="background: rgba(255,92,22,0.15);"
				aria-label="완료"
			>
				<svg
					class="h-[13px] w-[13px]"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#ff5c16"
					stroke-width="3"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M5 12l5 5L20 7" />
				</svg>
			</span>
		{:else if state === 'locked'}
			<span
				class="flex h-[32px] w-[32px] items-center justify-center rounded-[8px]"
				style="background: #1a1a1a;"
				aria-label="잠김"
			>
				<svg
					class="h-[15px] w-[15px]"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#656565"
					stroke-width="2"
				>
					<rect x="5" y="11" width="14" height="9" rx="2" />
					<path d="M8 11V7a4 4 0 018 0v4" />
				</svg>
			</span>
		{/if}
	</div>
</button>
