<script lang="ts">
	import { page } from '$app/stores'
	import type { LessonInLecture } from '$lib/api'
	import SessionItem from './SessionItem.svelte'
	import { LoginModal, savePendingAction } from '$lib/features/auth'
	import { useAuth } from '$lib/features/auth/stores/auth.svelte'

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

	const auth = useAuth()
	let showLoginModal = $state(false)
	let redirectUrl = $state('/home')

	function handleSessionClick(sessionId: number) {
		if (!auth.isAuthenticated) {
			savePendingAction({ type: 'access-session', sessionId })
			redirectUrl = $page.url.pathname
			showLoginModal = true
		}
	}
</script>

<div class="flex flex-col gap-4 pt-5 pb-[50px]">
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
				onclick={() => handleSessionClick(session.lesson_id)}
			/>
		{/each}
	</div>
</div>

<LoginModal
	bind:open={showLoginModal}
	message="세션을 시청하려면 로그인이 필요합니다"
	{redirectUrl}
/>

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
