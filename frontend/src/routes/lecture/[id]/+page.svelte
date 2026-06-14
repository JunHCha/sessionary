<script lang="ts">
	import { onMount } from 'svelte'
	import { page } from '$app/stores'
	import { getLectureLectureLectureIdGet, waitForApiInit } from '$lib/api'
	import type { LectureDetail } from '$lib/api'
	import { LoginModal, useAuth } from '$lib/features/auth'
	import { TicketConfirmModal, TicketInsufficientModal } from '$lib/features/ticket'
	import {
		LectureInfo,
		LectureMetaCard,
		LectureProgressPanel,
		SessionList,
		SheetPreview,
		createLectureAccess,
		getResumeLessonId,
		type LectureAccessController
	} from '$lib/features/lecture'

	let lecture = $state<LectureDetail | null>(null)
	let isLoading = $state(true)
	let activeTab = $state<'sessions' | 'sheet'>('sessions')

	const auth = useAuth()

	let access = $state<LectureAccessController | null>(null)

	async function fetchLecture(id: number) {
		await waitForApiInit()
		try {
			isLoading = true
			const response = await getLectureLectureLectureIdGet({ lectureId: id })
			lecture = response.data
		} catch (error) {
			console.error('Failed to fetch lecture:', error)
		} finally {
			isLoading = false
		}
	}

	$effect(() => {
		const id = Number($page.params.id)
		if (!isNaN(id) && id > 0) {
			access = createLectureAccess(id)
			fetchLecture(id)
		}
	})

	onMount(() => {
		access?.resumePendingSessionIfExists()
	})

	function handleSessionClick(sessionId: number) {
		access?.requestSession(sessionId)
	}

	function handleResume() {
		if (!lecture) return
		const target = getResumeLessonId(lecture.lessons, lecture.progress, auth.isAuthenticated)
		if (target != null) {
			access?.requestSession(target)
		}
	}
</script>

<main class="min-h-screen bg-[#0c0c0c] pt-[73px]">
	{#if isLoading}
		<div class="flex h-[60vh] items-center justify-center">
			<div
				class="h-12 w-12 animate-spin rounded-full border-4 border-brand-primary border-t-transparent"
			></div>
		</div>
	{:else if lecture}
		<div class="mx-auto w-full max-w-[1200px] px-5 pb-[120px] lg:px-10 lg:pb-16">
			<!-- HERO -->
			<section class="grid grid-cols-1 gap-8 pt-6 lg:grid-cols-[1.1fr_0.95fr] lg:gap-10">
				<LectureInfo {lecture} />
				<LectureProgressPanel
					sessions={lecture.lessons}
					progress={lecture.progress}
					isAuthenticated={auth.isAuthenticated}
					onstart={handleSessionClick}
					onlogin={() => access && (access.showLoginModal = true)}
				/>
			</section>

			<!-- Mobile tabs -->
			<div class="mt-8 flex border-b border-[#242424] lg:hidden">
				<button
					type="button"
					class="flex-1 py-3 text-[14px] font-semibold"
					style="color: {activeTab === 'sessions' ? '#f5f5f5' : '#848484'};"
					class:border-b-2={activeTab === 'sessions'}
					class:border-brand-primary={activeTab === 'sessions'}
					onclick={() => (activeTab = 'sessions')}
				>
					세션 목록
				</button>
				<button
					type="button"
					class="flex-1 py-3 text-[14px] font-semibold"
					style="color: {activeTab === 'sheet' ? '#f5f5f5' : '#848484'};"
					class:border-b-2={activeTab === 'sheet'}
					class:border-brand-primary={activeTab === 'sheet'}
					onclick={() => (activeTab = 'sheet')}
				>
					악보
				</button>
			</div>

			<!-- LOWER: sessions + aside -->
			<section class="mt-8 grid grid-cols-1 gap-10 lg:mt-12 lg:grid-cols-[1fr_340px] lg:items-start">
				<div class:hidden={activeTab !== 'sessions'} class="lg:block">
					<SessionList
						sessions={lecture.lessons}
						progress={lecture.progress}
						onSessionClick={handleSessionClick}
					/>
				</div>

				<aside
					class:hidden={activeTab !== 'sheet'}
					class="flex flex-col gap-[18px] lg:sticky lg:top-5 lg:block lg:space-y-[18px]"
				>
					<SheetPreview />
					<LectureMetaCard {lecture} />
				</aside>
			</section>
		</div>

		<!-- Mobile fixed CTA -->
		<div
			class="fixed bottom-0 left-0 right-0 z-20 flex gap-[10px] bg-gradient-to-t from-[#0c0c0c] to-transparent px-5 pb-6 pt-4 lg:hidden"
		>
			<button
				type="button"
				data-testid="mobile-resume-cta"
				class="flex h-[52px] flex-1 items-center justify-center gap-2 rounded-[12px] bg-[#ff5c16] text-[16px] font-bold text-white"
				onclick={handleResume}
			>
				<svg class="h-[18px] w-[18px]" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z" /></svg>
				{auth.isAuthenticated && lecture.progress && lecture.progress.completed_count > 0
					? '이어서 수강하기'
					: '수강 시작하기'}
			</button>
			<button
				type="button"
				aria-label="악보"
				class="flex h-[52px] w-[52px] items-center justify-center rounded-[12px] border border-[#333] bg-[#141414]"
				onclick={() => (activeTab = 'sheet')}
			>
				<svg
					class="h-[20px] w-[20px]"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#f5f5f5"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M16 12l-4 4-4-4M12 16V4" />
				</svg>
			</button>
		</div>
	{:else}
		<div class="flex h-[60vh] items-center justify-center">
			<p class="text-xl text-content-secondary">렉처를 찾을 수 없습니다.</p>
		</div>
	{/if}

	{#if access}
		<LoginModal bind:open={access.showLoginModal} redirectUrl={$page.url.pathname} />
		<TicketConfirmModal
			bind:open={access.showConfirmModal}
			lectureTitle={lecture?.title ?? ''}
			lectureThumbnail={lecture?.thumbnail}
			ticketCount={access.ticketCount}
			onConfirm={() => access?.confirmTicket()}
			onCancel={() => access?.cancelTicket()}
		/>
		<TicketInsufficientModal
			bind:open={access.showInsufficientModal}
			daysUntilRefill={access.daysUntilRefill}
			onClose={() => access?.closeInsufficient()}
		/>
	{/if}
</main>
