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

<div class="flex flex-col gap-4">
	<div class="flex items-center justify-between">
		<h2 class="text-2xl font-pretendard font-bold text-white">세션 목록</h2>
		<div class="flex items-center gap-2 text-content-secondary">
			<span class="text-brand-primary font-bold">{currentSessionIndex}</span>
			<span>/</span>
			<span>{sessions.length}</span>
		</div>
	</div>

	<div class="flex flex-col gap-2 max-h-[60vh] overflow-y-auto pr-2 custom-scrollbar">
		{#each sortedSessions as session, idx}
			<SessionItem {session} index={idx} isCurrent={idx === currentSessionIndex} />
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
