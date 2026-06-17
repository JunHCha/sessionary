import { goto } from '$app/navigation'
import {
	getLectureAccessStatusTicketLectureLectureIdGet,
	useTicketTicketLectureLectureIdPost,
	waitForApiInit
} from '$lib/api'
import { useAuth } from '$lib/features/auth'
import {
	savePendingSessionIdToStorage,
	getPendingSessionIdFromStorage,
	isUnauthorizedApiError
} from '../components/SessionList.svelte'

export type LectureAccessController = ReturnType<typeof createLectureAccess>

export function createLectureAccess(lectureId: number) {
	const auth = useAuth()

	let showLoginModal = $state(false)
	let showConfirmModal = $state(false)
	let showInsufficientModal = $state(false)
	let ticketCount = $state(0)
	let daysUntilRefill = $state(0)
	let accessible = $state<boolean | null>(null)
	let pendingSessionId: number | null = null

	async function loadAccessStatus() {
		if (!auth.isAuthenticated) return
		await waitForApiInit()
		try {
			const status = await getLectureAccessStatusTicketLectureLectureIdGet({ lectureId })
			accessible = status.accessible
			ticketCount = status.ticket_count
		} catch {
			accessible = null
		}
	}

	function calculateDaysUntilNextMonday(): number {
		const now = new Date()
		const currentDay = now.getDay()
		return (8 - currentDay) % 7 || 7
	}

	function showLoginPrompt(sessionId: number) {
		pendingSessionId = sessionId
		savePendingSessionIdToStorage(sessionId)
		showLoginModal = true
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
			daysUntilRefill = calculateDaysUntilNextMonday()
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

	async function checkAccessAndProceed(sessionId: number) {
		await waitForApiInit()
		try {
			const status = await getLectureAccessStatusTicketLectureLectureIdGet({ lectureId })
			if (status.accessible) {
				navigateToSession(sessionId)
			} else {
				handleTicketRequired(sessionId, status.ticket_count)
			}
		} catch (error) {
			handleAccessCheckError(error, sessionId)
		}
	}

	async function requestSession(sessionId: number) {
		if (!auth.isAuthenticated) {
			showLoginPrompt(sessionId)
			return
		}
		await checkAccessAndProceed(sessionId)
	}

	function resumePendingSessionIfExists() {
		if (!auth.isAuthenticated) return
		const sessionId = getPendingSessionIdFromStorage()
		if (sessionId !== null) {
			checkAccessAndProceed(sessionId)
		}
	}

	async function confirmTicket() {
		if (pendingSessionId === null) return
		try {
			await useTicketTicketLectureLectureIdPost({ lectureId })
			showConfirmModal = false
			goto(`/session/${pendingSessionId}`)
		} catch (error) {
			if (isUnauthorizedApiError(error)) {
				showConfirmModal = false
				showLoginPrompt(pendingSessionId)
				return
			}
			console.error('Failed to use ticket:', error)
		}
	}

	function cancelTicket() {
		showConfirmModal = false
		pendingSessionId = null
	}

	function closeInsufficient() {
		showInsufficientModal = false
	}

	return {
		get showLoginModal() {
			return showLoginModal
		},
		set showLoginModal(v: boolean) {
			showLoginModal = v
		},
		get showConfirmModal() {
			return showConfirmModal
		},
		set showConfirmModal(v: boolean) {
			showConfirmModal = v
		},
		get showInsufficientModal() {
			return showInsufficientModal
		},
		set showInsufficientModal(v: boolean) {
			showInsufficientModal = v
		},
		get ticketCount() {
			return ticketCount
		},
		get daysUntilRefill() {
			return daysUntilRefill
		},
		get accessible() {
			return accessible
		},
		loadAccessStatus,
		requestSession,
		resumePendingSessionIfExists,
		confirmTicket,
		cancelTicket,
		closeInsufficient
	}
}
