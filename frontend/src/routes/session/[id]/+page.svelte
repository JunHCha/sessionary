<script lang="ts">
	import { page } from '$app/stores'
	import {
		VideoPlayerPlaceholder,
		SubtitlePanelPlaceholder,
		TabSheetPlaceholder,
		PlayingGuidePlaceholder
	} from '$lib/features/session'

	// Mock data
	const mockSession = {
		id: 1,
		title: 'Session Title',
		currentIndex: 1,
		totalSessions: 10
	}

	let sessionId = $derived(Number($page.params.id))
	let currentIndex = $state(mockSession.currentIndex)
	let totalSessions = $state(mockSession.totalSessions)

	function goToPrevious() {
		if (currentIndex > 1) {
			currentIndex--
		}
	}

	function goToNext() {
		if (currentIndex < totalSessions) {
			currentIndex++
		}
	}
</script>

<main data-testid="session-detail-page" class="min-h-screen bg-[#0c0c0c] pt-[73px]">
	<div class="max-w-[1400px] mx-auto px-6 py-6">
		<!-- Top Row: Video Player + Subtitle Panel -->
		<div class="flex gap-4 mb-4">
			<div class="flex-[2]">
				<VideoPlayerPlaceholder />
			</div>
			<div class="flex-1">
				<SubtitlePanelPlaceholder />
			</div>
		</div>

		<!-- Tab Sheet -->
		<div class="mb-4">
			<TabSheetPlaceholder />
		</div>

		<!-- Playing Guide -->
		<div class="mb-4">
			<PlayingGuidePlaceholder />
		</div>

		<!-- Session Navigation -->
		<nav
			data-testid="session-navigation"
			class="flex items-center justify-center gap-8 py-4 bg-[#1a1a1a] rounded-lg"
		>
			<button
				type="button"
				onclick={goToPrevious}
				disabled={currentIndex <= 1}
				class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
				</svg>
				<span>이전 세션</span>
			</button>

			<div class="text-white font-medium">
				<span class="text-brand-primary">{String(currentIndex).padStart(2, '0')}</span>
				<span class="text-[#666] mx-2">/</span>
				<span>{String(totalSessions).padStart(2, '0')}</span>
			</div>

			<button
				type="button"
				onclick={goToNext}
				disabled={currentIndex >= totalSessions}
				class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
			>
				<span>다음 세션</span>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</button>
		</nav>
	</div>
</main>
