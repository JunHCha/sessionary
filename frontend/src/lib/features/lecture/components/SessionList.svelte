<script lang="ts">
	import { goto } from '$app/navigation'
	import type { LessonInLecture } from '$lib/api'
	import {
		getLectureAccessStatusTicketLectureLectureIdGet,
		useTicketTicketLectureLectureIdPost,
		waitForApiInit
	} from '$lib/api'
	import { TicketConfirmModal, TicketInsufficientModal } from '$lib/features/ticket'
	import SessionItem from './SessionItem.svelte'

	let {
		sessions,
		lectureId,
		lectureTitle,
		lectureThumbnail,
		currentSessionIndex = 0
	}: {
		sessions: LessonInLecture[]
		lectureId: number
		lectureTitle: string
		lectureThumbnail: string
		currentSessionIndex?: number
	} = $props()

	let sortedSessions = $derived(
		[...sessions].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
	)

	let showConfirmModal = $state(false)
	let showInsufficientModal = $state(false)
	let ticketCount = $state(0)
	let daysUntilRefill = $state(0)
	let pendingSessionId: number | null = null

	async function handleSessionClick(sessionId: number) {
		await waitForApiInit()
		try {
			// Check lecture access status
			const status = await getLectureAccessStatusTicketLectureLectureIdGet({
				lectureId
			})

			if (status.accessible) {
				// Already has access, go directly to session
				goto(`/session/${sessionId}`)
			} else {
				// Need to use ticket
				ticketCount = status.ticket_count
				if (status.ticket_count > 0) {
					// Show confirmation modal
					pendingSessionId = sessionId
					showConfirmModal = true
				} else {
					// Show insufficient modal
					// TODO: Calculate actual days until refill
					daysUntilRefill = 7
					showInsufficientModal = true
				}
			}
		} catch (error) {
			console.error('Failed to check lecture access:', error)
		}
	}

	async function handleConfirm() {
		if (pendingSessionId === null) return

		try {
			await useTicketTicketLectureLectureIdPost({ lectureId })
			showConfirmModal = false
			goto(`/session/${pendingSessionId}`)
		} catch (error) {
			console.error('Failed to use ticket:', error)
		}
	}

	function handleCancel() {
		showConfirmModal = false
		pendingSessionId = null
	}

	function handleInsufficientClose() {
		showInsufficientModal = false
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
				onclick={() => handleSessionClick(session.id)}
			/>
		{/each}
	</div>
</div>

<TicketConfirmModal
	bind:open={showConfirmModal}
	{lectureTitle}
	{lectureThumbnail}
	{ticketCount}
	onConfirm={handleConfirm}
	onCancel={handleCancel}
/>

<TicketInsufficientModal
	bind:open={showInsufficientModal}
	{daysUntilRefill}
	onClose={handleInsufficientClose}
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
