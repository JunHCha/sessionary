<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { waitForApiInit } from '$lib/api/config'
	import {
		VideoPlayer,
		SubtitlePanelPlaceholder,
		TabSheetPlaceholder,
		PlayingGuidePlaceholder,
		loadSessionDetail,
		type SessionDetailData
	} from '$lib/features/session'

	let { data } = $props()

	let session = $state<SessionDetailData | null>(null)
	let loading = $state(true)
	let error = $state<string | null>(null)
	let currentTime = $state(0)

	onMount(async () => {
		try {
			await waitForApiInit()
			session = await loadSessionDetail(data.sessionId)
		} catch (e) {
			error = e instanceof Error ? e.message : '세션을 불러올 수 없습니다'
		} finally {
			loading = false
		}
	})

	function goToPrevious() {
		if (session?.prevSessionId) {
			goto(`/session/${session.prevSessionId}`)
		}
	}

	function goToNext() {
		if (session?.nextSessionId) {
			goto(`/session/${session.nextSessionId}`)
		}
	}
</script>

<main data-testid="session-detail-page" class="min-h-screen bg-[#0c0c0c] pt-[73px]">
	<div class="max-w-[1400px] mx-auto px-6 py-6">
		{#if loading}
			<div data-testid="session-loading" class="flex items-center justify-center h-[60vh]">
				<div class="text-[#999] text-lg">로딩 중...</div>
			</div>
		{:else if error}
			<div data-testid="session-error" class="flex items-center justify-center h-[60vh]">
				<div class="text-red-400 text-lg">{error}</div>
			</div>
		{:else if session}
			<!-- Top Row: Video Player + Subtitle Panel -->
			<div class="flex gap-4 mb-4">
				<div class="flex-[2]">
					<VideoPlayer
						src={session.videoUrl}
						ontimeupdate={(e) => (currentTime = e.currentTime)}
					/>
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
					disabled={!session.prevSessionId}
					class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 19l-7-7 7-7"
						/>
					</svg>
					<span>이전 세션</span>
				</button>

				<div class="text-white font-medium">
					<span class="text-brand-primary"
						>{String(session.lectureOrdering).padStart(2, '0')}</span
					>
					<span class="text-[#666] mx-2">/</span>
					<span>{String(session.totalSessions).padStart(2, '0')}</span>
				</div>

				<button
					type="button"
					onclick={goToNext}
					disabled={!session.nextSessionId}
					class="flex items-center gap-2 px-4 py-2 text-sm text-[#999] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					<span>다음 세션</span>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5l7 7-7 7"
						/>
					</svg>
				</button>
			</nav>
		{/if}
	</div>
</main>
