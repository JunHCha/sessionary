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
				const parsed = parseInt(id, 10)
				return Number.isNaN(parsed) ? null : parsed
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

	export function calculateDaysUntilNextMonday(): number {
		const now = new Date()
		const currentDay = now.getDay()
		const daysUntilMonday = (8 - currentDay) % 7 || 7
		return daysUntilMonday
	}
</script>

<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import { useAuth } from '$lib/features/auth'
	import { getSessionState, type LectureProgress } from '../utils/progress'
	import SessionItem from './SessionItem.svelte'

	let {
		sessions,
		progress = null,
		onSessionClick
	}: {
		sessions: LessonInLecture[]
		progress?: LectureProgress | null
		onSessionClick: (sessionId: number) => void
	} = $props()

	const auth = useAuth()

	let sortedSessions = $derived(
		[...sessions].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
	)

	let completedCount = $derived(progress?.completed_count ?? 0)
</script>

<div class="flex flex-col gap-4">
	<div class="flex items-baseline gap-3 border-b border-[#242424] pb-[14px]">
		<h2
			class="text-[19px] font-bold"
			style="font-family: Helvetica, Arial, sans-serif; color: #f5f5f5;"
		>
			세션 목록
		</h2>
		<span class="text-[13px] text-[#656565]">
			전체 {sortedSessions.length}개 · {completedCount}개 완료
		</span>
	</div>

	<div class="flex flex-col gap-[10px]">
		{#each sortedSessions as session, idx}
			<SessionItem
				{session}
				index={idx}
				state={getSessionState(session.id, progress, auth.isAuthenticated)}
				onclick={() => onSessionClick(session.id)}
			/>
		{/each}
	</div>
</div>
