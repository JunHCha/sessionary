<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import { waitForApiInit, getLecturesLectureGet, createLectureLecturePost } from '$lib/api'
	import type { LectureInList } from '$lib/api'
	import { getThumbnailSrc } from '$lib/features/lecture/utils/format'

	let lectures = $state<LectureInList[]>([])
	let title = $state('')
	let description = $state('')
	let creating = $state(false)
	let error = $state('')
	let loading = $state(true)
	let createOpen = $state(true)
	let search = $state('')

	let page = $state(1)
	let totalPages = $state(1)
	let totalItems = $state(0)

	const filtered = $derived(
		search.trim()
			? lectures.filter((l) => l.title.toLowerCase().includes(search.trim().toLowerCase()))
			: lectures
	)

	function tagLabels(tags: unknown[] | null): string[] {
		if (!tags || !Array.isArray(tags)) return []
		return tags.map((t) => String(t))
	}

	onMount(async () => {
		await waitForApiInit()
		await loadLectures()
	})

	async function loadLectures() {
		loading = true
		try {
			// 1페이지는 파라미터 없이 요청해 기본 동작을 유지하고, 이후 페이지만 명시적으로 전달
			const res = await getLecturesLectureGet(page > 1 ? { page, perPage: 20 } : {})
			lectures = res.data ?? []
			const meta = res.meta as { total_pages?: number; total_items?: number } | undefined
			totalPages = meta?.total_pages ?? 1
			totalItems = meta?.total_items ?? lectures.length
		} catch (e) {
			error = '렉처 목록을 불러오지 못했습니다'
			console.error(e)
		} finally {
			loading = false
		}
	}

	async function goToPage(next: number) {
		if (next < 1 || next > totalPages || next === page) return
		page = next
		search = ''
		await loadLectures()
	}

	async function createLecture() {
		if (!title.trim()) return
		creating = true
		error = ''
		try {
			const res = await createLectureLecturePost({
				requestBody: { title: title.trim(), description: description.trim() }
			})
			const created = res.data
			lectures = [
				{
					id: created.id,
					thumbnail: created.thumbnail,
					title: created.title,
					artist: created.artist,
					lessons: created.lessons,
					description: created.description,
					tags: created.tags,
					length_sec: created.length_sec,
					lecture_count: created.lecture_count,
					time_created: created.time_created,
					time_updated: created.time_updated
				},
				...lectures
			]
			totalItems += 1
			title = ''
			description = ''
			createOpen = false
		} catch (e) {
			error = '렉처 생성에 실패했습니다'
			console.error(e)
		} finally {
			creating = false
		}
	}
</script>

<div class="flex flex-col gap-8 font-pretendard">
	<header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
		<div class="flex flex-col gap-2">
			<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
				Lectures
			</span>
			<h1 class="text-[28px] font-bold leading-tight tracking-[-0.02em] sm:text-[32px]">
				렉처 관리
			</h1>
			<p class="text-[14px] text-[#848484]">
				총 <span class="font-semibold text-white">{totalItems}</span>개의 렉처
			</p>
		</div>
		<button
			type="button"
			data-testid="toggle-create-lecture"
			onclick={() => (createOpen = !createOpen)}
			class="inline-flex shrink-0 items-center gap-1.5 rounded-xl border px-4 py-2.5 text-[14px] font-semibold transition-colors
				{createOpen
				? 'border-[#FF5C16]/50 bg-[#FF5C16]/12 text-[#FF8B5C]'
				: 'border-white/[0.1] bg-[#161616] text-white hover:border-[#FF5C16]/50'}"
			aria-expanded={createOpen}
		>
			<svg
				class="h-4 w-4 transition-transform duration-200 {createOpen ? 'rotate-45' : ''}"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2.2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M12 5v14M5 12h14" />
			</svg>
			새 렉처
		</button>
	</header>

	<!-- 새 렉처 카드 (별도 분리, 토글) -->
	{#if createOpen}
		<section
			class="overflow-hidden rounded-2xl border border-[#FF5C16]/25 bg-[#141414]"
			data-testid="create-lecture-panel"
		>
			<div class="h-0.5 w-full bg-gradient-to-r from-[#FF5C16] to-[#FF8B5C]"></div>
			<div class="flex flex-col gap-4 p-5">
				<h2 class="text-[15px] font-bold tracking-[-0.01em]">새 렉처 만들기</h2>
				<div class="grid gap-4 sm:grid-cols-2">
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						제목
						<input
							data-testid="lecture-title-input"
							bind:value={title}
							placeholder="렉처 제목"
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white placeholder:text-[#5a5a5a] outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						설명
						<input
							data-testid="lecture-desc-input"
							bind:value={description}
							placeholder="렉처 설명 (선택)"
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white placeholder:text-[#5a5a5a] outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
				</div>
				<div>
					<Button
						data-testid="create-lecture-btn"
						color="primary"
						class="font-pretendard font-semibold"
						disabled={creating}
						onclick={createLecture}
					>
						{creating ? '생성 중...' : '렉처 생성'}
					</Button>
				</div>
			</div>
		</section>
	{/if}

	<!-- 검색 -->
	<div class="relative">
		<svg
			class="pointer-events-none absolute left-3.5 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-[#656565]"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="1.8"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<circle cx="11" cy="11" r="7" />
			<path d="m21 21-4.3-4.3" />
		</svg>
		<input
			data-testid="lecture-search-input"
			bind:value={search}
			placeholder="제목으로 검색"
			class="w-full rounded-xl border border-white/[0.08] bg-[#141414] py-2.5 pl-11 pr-4 text-[14px] text-white placeholder:text-[#656565] outline-none transition-colors focus:border-[#FF5C16]"
		/>
	</div>

	{#if error}
		<p
			class="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2.5 text-[13px] text-red-300"
			data-testid="lecture-error"
		>
			{error}
		</p>
	{/if}

	<!-- 목록 -->
	{#if loading}
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each Array(6) as _, i (i)}
				<div
					class="h-[212px] animate-pulse rounded-2xl border border-white/[0.05] bg-[#121212]"
				></div>
			{/each}
		</div>
	{:else if filtered.length === 0}
		<div
			class="flex flex-col items-center gap-2 rounded-2xl border border-dashed border-white/[0.1] bg-[#101010] py-16 text-center"
			data-testid="lectures-empty"
		>
			<p class="text-[15px] font-semibold text-white">
				{search.trim() ? '검색 결과가 없습니다' : '아직 렉처가 없습니다'}
			</p>
			<p class="text-[13px] text-[#656565]">
				{search.trim() ? '다른 키워드로 검색해 보세요' : "'새 렉처'로 첫 렉처를 추가하세요"}
			</p>
		</div>
	{:else}
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each filtered as lecture (lecture.id)}
				<a
					href={`/admin/lectures/${lecture.id}`}
					data-testid="lecture-row"
					class="group flex flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414] transition-all duration-200 hover:-translate-y-0.5 hover:border-[#FF5C16]/50 hover:bg-[#171717]"
				>
					<div class="relative aspect-[16/9] w-full overflow-hidden bg-[#1d1d1d]">
						<img
							src={getThumbnailSrc(lecture.thumbnail)}
							alt={lecture.title}
							class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
						/>
						<span
							class="absolute right-2.5 top-2.5 rounded-md bg-black/60 px-2 py-0.5 text-[11px] font-medium text-[#cfcfcf] backdrop-blur-sm"
						>
							#{lecture.id}
						</span>
					</div>
					<div class="flex flex-1 flex-col gap-2.5 p-4">
						<h3
							class="line-clamp-2 text-[15px] font-bold leading-snug tracking-[-0.01em] transition-colors group-hover:text-[#FF5C16]"
						>
							{lecture.title}
						</h3>
						<div class="mt-auto flex flex-wrap items-center gap-1.5">
							<span
								class="inline-flex items-center gap-1 rounded-md bg-white/[0.05] px-2 py-0.5 text-[11px] font-medium text-[#9a9a9a]"
							>
								레슨 {lecture.lessons?.length ?? 0}
							</span>
							{#each tagLabels(lecture.tags).slice(0, 2) as tag (tag)}
								<span
									class="inline-flex items-center rounded-md bg-[#FF5C16]/12 px-2 py-0.5 text-[11px] font-medium text-[#FF8B5C]"
								>
									{tag}
								</span>
							{/each}
						</div>
					</div>
				</a>
			{/each}
		</div>

		<!-- 페이지네이션 -->
		{#if totalPages > 1}
			<nav
				class="flex items-center justify-center gap-1.5 pt-1"
				aria-label="페이지네이션"
				data-testid="lectures-pagination"
			>
				<button
					type="button"
					data-testid="page-prev"
					aria-label="이전 페이지"
					disabled={page <= 1}
					onclick={() => goToPage(page - 1)}
					class="flex h-9 w-9 items-center justify-center rounded-lg border border-white/[0.08] text-[#9a9a9a] transition-colors hover:border-[#FF5C16]/50 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
				>
					<svg
						class="h-4 w-4"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M15 6l-6 6 6 6" />
					</svg>
				</button>
				{#each Array(totalPages) as _, i (i)}
					{@const p = i + 1}
					<button
						type="button"
						data-testid={`page-${p}`}
						aria-current={p === page ? 'page' : undefined}
						onclick={() => goToPage(p)}
						class="flex h-9 min-w-9 items-center justify-center rounded-lg border px-2.5 text-[13px] font-semibold transition-colors
							{p === page
							? 'border-[#FF5C16] bg-[#FF5C16]/12 text-white'
							: 'border-white/[0.08] text-[#9a9a9a] hover:border-[#FF5C16]/50 hover:text-white'}"
					>
						{p}
					</button>
				{/each}
				<button
					type="button"
					data-testid="page-next"
					aria-label="다음 페이지"
					disabled={page >= totalPages}
					onclick={() => goToPage(page + 1)}
					class="flex h-9 w-9 items-center justify-center rounded-lg border border-white/[0.08] text-[#9a9a9a] transition-colors hover:border-[#FF5C16]/50 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
				>
					<svg
						class="h-4 w-4"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6" />
					</svg>
				</button>
			</nav>
		{/if}
	{/if}
</div>
