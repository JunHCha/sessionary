<script lang="ts" module>
	export function savePendingSessionIdToStorage(sessionId: number): void {
		if (typeof sessionStorage !== 'undefined') {
			sessionStorage.setItem('pendingSessionId', sessionId.toString())
		}
	}

	export function getPendingSessionIdFromStorage(): number | null {
		if (typeof sessionStorage !== 'undefined') {
			const id = sessionStorage.getItem('pendingSessionId')
			if (id) {
				sessionStorage.removeItem('pendingSessionId')
				return parseInt(id, 10)
			}
		}
		return null
	}

	export function isUnauthorizedApiError(error: unknown): boolean {
		return (
			typeof error === 'object' &&
			error !== null &&
			'status' in error &&
			error.status === 401
		)
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { page } from '$app/stores'
	import type { LessonInLecture } from '$lib/api'
	import {
		getLectureAccessStatusTicketLectureLectureIdGet,
		useTicketTicketLectureLectureIdPost,
		waitForApiInit
	} from '$lib/api'
	import { LoginModal, useAuth } from '$lib/features/auth'
	import { TicketConfirmModal, TicketInsufficientModal } from '$lib/features/ticket'
	import SessionItem from './SessionItem.svelte'

	let {
		sessions,
		lectureId,
		lectureTitle,
		currentSessionIndex = 0
	}: {
		sessions: LessonInLecture[]
		lectureId: number
		lectureTitle: string
		currentSessionIndex?: number
	} = $props()

	let sortedSessions = $derived(
		[...sessions].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
	)

	let showLoginModal = $state(false)
	let showConfirmModal = $state(false)
	let showInsufficientModal = $state(false)
	let ticketCount = $state(0)
	let daysUntilRefill = $state(0)
	let pendingSessionId: number | null = null

	const auth = useAuth()

	onMount(() => {
		resumePendingSessionIfExists()
	})

	function resumePendingSessionIfExists() {
		if (!auth.isAuthenticated) return

		const sessionId = getPendingSessionIdFromStorage()
		if (sessionId !== null) {
			checkAccessAndProceed(sessionId)
		}
	}

	async function handleSessionClick(sessionId: number) {
		if (!auth.isAuthenticated) {
			showLoginPrompt(sessionId)
			return
		}

		await checkAccessAndProceed(sessionId)
	}

	function showLoginPrompt(sessionId: number) {
		pendingSessionId = sessionId
		savePendingSessionIdToStorage(sessionId)
		showLoginModal = true
	}

	async function checkAccessAndProceed(sessionId: number) {
		await waitForApiInit()
		try {
			const status = await getLectureAccessStatusTicketLectureLectureIdGet({
				lectureId
			})

			if (status.accessible) {
				navigateToSession(sessionId)
			} else {
				handleTicketRequired(sessionId, status.ticket_count)
			}
		} catch (error) {
			handleAccessCheckError(error, sessionId)
		}
	}

	function navigateToSession(sessionId: number) {
		goto(`/session/${sessionId}`)
	}

	function handleTicketRequired(sessionId: number, availableTickets: number) {
		ticketCount = availableTickets
		if (availableTickets > 0) {
			pendingSessionId = sessionId
			showConfirmModal = true
		} else {
			daysUntilRefill = 7
			showInsufficientModal = true
		}
	}

	function handleAccessCheckError(error: unknown, sessionId: number) {
		if (isUnauthorizedApiError(error)) {
			showLoginPrompt(sessionId)
		} else {
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
	
	function getRedirectUrl(): string {
		return $page.url.pathname
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

<LoginModal bind:open={showLoginModal} redirectUrl={getRedirectUrl()} />

<TicketConfirmModal
	bind:open={showConfirmModal}
	{lectureTitle}
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
