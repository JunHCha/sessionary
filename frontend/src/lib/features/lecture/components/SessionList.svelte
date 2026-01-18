<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import SessionItem from './SessionItem.svelte'

	let {
		sessions,
		currentSessionIndex = 0
	}: {
		sessions: LessonInLecture[]
		currentSessionIndex?: number
	} = $props()

	let sortedSessions = $derived(
		[...sessions].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
	)
</script>

<div class="flex flex-col gap-4 pt-5 pb-[50px] px-[55px]">
	<h2
		class="text-[28px] font-bold"
		style="font-family: Helvetica, Arial, sans-serif; color: #f5f5f5;"
	>
		세션 목록
	</h2>

	<div class="flex flex-col gap-3 max-h-[80vh] overflow-y-auto pr-2 custom-scrollbar">
		{#each sortedSessions as session, idx}
			<SessionItem
				{session}
				index={idx}
				isCurrent={idx === currentSessionIndex}
				isCompleted={false}
			/>
		{/each}
	</div>
</div>

<style>
	.custom-scrollbar::-webkit-scrollbar {
		width: 6px;
	}
	.custom-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}
	.custom-scrollbar::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}
	.custom-scrollbar::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.2);
	}
</style>
