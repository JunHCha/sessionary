<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import { getLectureStatusMode, type LectureProgress } from '../utils/progress'
	import { buildMinimap, getFirstLessonId, getResumeLessonId } from '../utils/curriculum'

	let {
		sessions,
		progress = null,
		isAuthenticated = false,
		accessible = null,
		onstart,
		onlogin
	}: {
		sessions: LessonInLecture[]
		progress?: LectureProgress | null
		isAuthenticated?: boolean
		accessible?: boolean | null
		onstart?: (lessonId: number) => void
		onlogin?: () => void
	} = $props()

	let sortedSessions = $derived(
		[...sessions].sort((a, b) => a.lecture_ordering - b.lecture_ordering)
	)

	let mode = $derived(getLectureStatusMode(progress, isAuthenticated, accessible))
	let cells = $derived(buildMinimap(sortedSessions, progress, isAuthenticated))

	let resumeLessonId = $derived(getResumeLessonId(sortedSessions, progress, isAuthenticated))
	let firstLessonId = $derived(getFirstLessonId(sortedSessions))

	let resumeLesson = $derived(
		sortedSessions.find((s) => s.id === (resumeLessonId ?? firstLessonId)) ?? null
	)
	let resumeIndex = $derived(
		resumeLesson ? sortedSessions.findIndex((s) => s.id === resumeLesson!.id) : 0
	)
	let resumeNumber = $derived(String(resumeIndex + 1).padStart(2, '0'))

	let totalCount = $derived(progress?.total_count ?? sortedSessions.length)
	let completedCount = $derived(progress?.completed_count ?? 0)
	let percent = $derived(progress?.percent ?? 0)

	// ring geometry: r=54 → circumference ≈ 339.29
	const CIRC = 2 * Math.PI * 54
	let dashOffset = $derived(CIRC * (1 - percent / 100))

	function handlePrimary() {
		if (mode === 'anonymous') {
			onlogin?.()
			return
		}
		const target = resumeLesson?.id ?? firstLessonId
		if (target != null) {
			onstart?.(target)
		}
	}
</script>

<div
	data-testid="lecture-progress-panel"
	data-mode={mode}
	class="flex min-h-[296px] flex-col rounded-[14px] border border-[#242424] bg-[#141414] p-[22px] lg:p-[26px]"
>
	{#if mode === 'in-progress'}
		<div class="mb-[18px] flex items-center justify-between">
			<span class="text-[15px] font-semibold text-[#c9c9c9]">커리큘럼</span>
			<span class="text-[13px] text-[#656565]">{completedCount} / {totalCount} 세션</span>
		</div>
		<div class="flex items-center gap-[26px]">
			<svg class="h-[126px] w-[126px] flex-shrink-0" viewBox="0 0 126 126">
				<circle cx="63" cy="63" r="54" fill="none" stroke="#242424" stroke-width="10" />
				<circle
					cx="63"
					cy="63"
					r="54"
					fill="none"
					stroke="#ff5c16"
					stroke-width="10"
					stroke-linecap="round"
					stroke-dasharray={CIRC}
					stroke-dashoffset={dashOffset}
					transform="rotate(-90 63 63)"
				/>
				<text
					x="63"
					y="60"
					text-anchor="middle"
					font-size="25"
					font-weight="700"
					fill="#fff"
				>
					{percent}%
				</text>
				<text x="63" y="80" text-anchor="middle" font-size="11" fill="#848484">완료</text>
			</svg>
			<div class="min-w-0">
				<div class="text-[12px] font-bold tracking-wide text-[#ff5c16]">이어보기</div>
				<div class="mt-[5px] text-[17px] font-bold leading-[1.35] text-white">
					{resumeNumber}. {resumeLesson?.title ?? ''}
				</div>
			</div>
		</div>
	{:else if mode === 'not-started'}
		<span
			data-testid="not-started-badge"
			class="mb-[18px] self-start rounded-full bg-[#1a1a1a] px-[11px] py-[4px] text-[12px] font-bold text-[#848484]"
		>
			미수강
		</span>
		<div class="mb-[18px] flex items-center justify-between opacity-50">
			<span class="text-[15px] font-semibold text-[#c9c9c9]">커리큘럼</span>
			<span class="text-[13px] text-[#656565]">0 / {totalCount} 세션</span>
		</div>
		<div class="min-w-0 opacity-50">
			<div class="text-[12px] font-bold tracking-wide text-[#848484]">시작하기</div>
			<div class="mt-[5px] text-[17px] font-bold leading-[1.35] text-white">
				{resumeNumber}. {resumeLesson?.title ?? ''}
			</div>
		</div>
	{:else}
		<span
			class="mb-[18px] self-start rounded-full bg-[#1a1a1a] px-[11px] py-[4px] text-[12px] font-bold text-[#848484]"
		>
			비로그인
		</span>
		<div
			class="flex flex-1 flex-col items-center justify-center gap-[8px] py-[20px] text-center"
		>
			<span
				class="flex h-[44px] w-[44px] items-center justify-center rounded-full bg-[#1a1a1a]"
			>
				<svg
					class="h-[20px] w-[20px]"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#848484"
					stroke-width="2"
				>
					<rect x="5" y="11" width="14" height="9" rx="2" />
					<path d="M8 11V7a4 4 0 018 0v4" />
				</svg>
			</span>
			<span class="text-[13px] text-[#848484]">로그인하면 수강을<br />시작할 수 있어요</span>
		</div>
	{/if}

	{#if mode !== 'anonymous'}
		<div class="mt-[18px] grid grid-cols-6 gap-[6px]" class:opacity-50={mode === 'not-started'}>
			{#each cells as cell}
				<span
					class="h-[9px] rounded-[3px]"
					class:bg-brand={cell === 'done'}
					style={cell === 'done'
						? 'background:#ff5c16'
						: cell === 'partial'
							? 'background:#5e3018'
							: cell === 'current'
								? `background:transparent;border:1.5px solid ${mode === 'not-started' ? '#3a3a3a' : '#ff5c16'}`
								: 'background:#1a1a1a'}
				></span>
			{/each}
		</div>
	{/if}

	<button
		type="button"
		data-testid="progress-panel-cta"
		class="mt-auto flex h-[48px] items-center justify-center gap-2 rounded-[11px] bg-[#ff5c16] text-[15px] font-bold text-white"
		onclick={handlePrimary}
	>
		{#if mode === 'anonymous'}
			로그인하고 시작
		{:else if mode === 'not-started'}
			<svg class="h-[17px] w-[17px]" viewBox="0 0 24 24" fill="#fff"
				><path d="M8 5v14l11-7z" /></svg
			>
			1강부터 시작하기
		{:else}
			<svg class="h-[17px] w-[17px]" viewBox="0 0 24 24" fill="#fff"
				><path d="M8 5v14l11-7z" /></svg
			>
			이어서 수강하기
		{/if}
	</button>
</div>
