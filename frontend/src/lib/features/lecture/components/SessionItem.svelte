<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import { formatDuration } from '../utils/format'

	let {
		session,
		index,
		isCurrent = false,
		isCompleted = false
	}: {
		session: LessonInLecture
		index: number
		isCurrent?: boolean
		isCompleted?: boolean
	} = $props()

	let displayNumber = $derived(String(index + 1).padStart(2, '0'))

	let numberColor = $derived(isCompleted ? '#444' : isCurrent ? '#ff5c16' : '#666')
</script>

<button
	type="button"
	class="w-full flex items-center h-[107px] px-[25px] rounded-xl transition-all duration-200 text-left"
	class:opacity-50={isCompleted}
	style={isCurrent
		? 'border: 1px solid #ff5c16; background: linear-gradient(to right, #1a1410, #0c0c0c); box-shadow: 0px 20px 25px -5px rgba(255,92,22,0.2), 0px 8px 10px -6px rgba(255,92,22,0.2);'
		: 'border: 1px solid #1f1f1f; background: #0c0c0c;'}
>
	<div class="flex items-center gap-[45px]">
		<div class="flex items-center gap-2">
			{#if isCurrent}
				<span
					class="px-2 py-0.5 rounded-full text-[10px] font-bold text-white"
					style="background: #ff5c16; font-family: Helvetica, Arial, sans-serif;"
				>
					NEXT
				</span>
			{/if}
			{#if isCompleted}
				<span class="w-2 h-2 rounded-full" style="background: #444;"></span>
			{/if}
			<span
				class="text-[20px] font-bold"
				style="color: {numberColor}; font-family: Helvetica, Arial, sans-serif;"
			>
				{displayNumber}
			</span>
		</div>

		<div class="flex-1 min-w-0">
			<p
				class="font-medium truncate"
				class:line-through={isCompleted}
				style="color: {isCompleted ? '#666' : isCurrent ? '#ffffff' : '#d5d5d5'};"
			>
				{session.title}
			</p>
		</div>
	</div>

	<div class="ml-auto flex-shrink-0">
		<span class="text-sm" style="color: {isCompleted ? '#555' : '#777'};">
			{formatDuration(session.length_sec)}
		</span>
	</div>
</button>
