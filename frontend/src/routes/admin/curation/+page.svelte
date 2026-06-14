<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import {
		waitForApiInit,
		getLecturesLectureGet,
		getCurationCurationGet,
		setCurationCurationSectionPut
	} from '$lib/api'
	import type { LectureInList, CurationSection } from '$lib/api'
	import { getThumbnailSrc } from '$lib/features/lecture/utils/format'

	const sections: CurationSection[] = ['TRENDING', 'NEW']
	const sectionLabel: Record<CurationSection, string> = {
		TRENDING: '요즘 많이 보는 렉처',
		NEW: '새로운 렉처'
	}
	const sectionTag: Record<CurationSection, string> = {
		TRENDING: '인기',
		NEW: '신규'
	}

	let candidates = $state<LectureInList[]>([])
	let selected = $state<Record<CurationSection, number[]>>({ TRENDING: [], NEW: [] })
	let saving = $state<Record<CurationSection, boolean>>({ TRENDING: false, NEW: false })
	let savedSection = $state<CurationSection | null>(null)
	let error = $state('')
	let search = $state('')

	const candidateMap = $derived(new Map(candidates.map((c) => [c.id, c])))

	const filteredCandidates = $derived(
		search.trim()
			? candidates.filter((c) => c.title.toLowerCase().includes(search.trim().toLowerCase()))
			: candidates
	)

	function tagLabels(tags: unknown[] | null): string[] {
		if (!tags || !Array.isArray(tags)) return []
		return tags.map((t) => String(t))
	}

	onMount(async () => {
		await waitForApiInit()
		try {
			const [lectures, curation] = await Promise.all([
				getLecturesLectureGet({}),
				getCurationCurationGet()
			])
			candidates = lectures.data ?? []
			selected = {
				TRENDING: (curation.data?.TRENDING ?? []).map((l) => l.id),
				NEW: (curation.data?.NEW ?? []).map((l) => l.id)
			}
		} catch (e) {
			error = '큐레이션 정보를 불러오지 못했습니다'
			console.error(e)
		}
	})

	function add(section: CurationSection, id: number) {
		if (selected[section].includes(id)) return
		selected[section] = [...selected[section], id]
	}

	function remove(section: CurationSection, id: number) {
		selected[section] = selected[section].filter((x) => x !== id)
	}

	function moveUp(section: CurationSection, index: number) {
		if (index <= 0) return
		const next = [...selected[section]]
		;[next[index - 1], next[index]] = [next[index], next[index - 1]]
		selected[section] = next
	}

	function moveDown(section: CurationSection, index: number) {
		if (index >= selected[section].length - 1) return
		const next = [...selected[section]]
		;[next[index + 1], next[index]] = [next[index], next[index + 1]]
		selected[section] = next
	}

	function titleOf(id: number): string {
		return candidateMap.get(id)?.title ?? `#${id}`
	}

	function thumbnailOf(id: number): string | null {
		return candidateMap.get(id)?.thumbnail ?? null
	}

	async function save(section: CurationSection) {
		saving[section] = true
		savedSection = null
		error = ''
		try {
			await setCurationCurationSectionPut({
				section,
				requestBody: { lecture_ids: selected[section] }
			})
			savedSection = section
		} catch (e) {
			error = '저장에 실패했습니다'
			console.error(e)
		} finally {
			saving[section] = false
		}
	}
</script>

<div class="flex flex-col gap-8 font-pretendard">
	<header class="flex flex-col gap-2">
		<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
			Home Curation
		</span>
		<h1 class="text-[28px] font-bold leading-tight tracking-[-0.02em] sm:text-[32px]">
			홈 큐레이션
		</h1>
		<p class="text-[14px] text-[#848484]">
			후보에서 렉처를 골라 섹션에 추가하고, 순서를 정한 뒤 섹션별로 저장하세요.
		</p>
	</header>

	{#if error}
		<p
			class="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2.5 text-[13px] text-red-300"
			data-testid="curation-error"
		>
			{error}
		</p>
	{/if}

	<!-- 선정 섹션 (2단 보드) -->
	<div class="grid gap-5 lg:grid-cols-2">
		{#each sections as section (section)}
			<section
				data-testid={`section-${section}`}
				class="flex flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]"
			>
				<div class="flex items-center justify-between border-b border-white/[0.06] px-5 py-4">
					<div class="flex items-center gap-2.5">
						<span
							class="rounded-md bg-[#FF5C16]/12 px-2 py-0.5 text-[11px] font-bold text-[#FF8B5C]"
						>
							{sectionTag[section]}
						</span>
						<h2 class="text-[15px] font-bold tracking-[-0.01em]">
							{sectionLabel[section]}
						</h2>
						<span
							class="rounded-md bg-white/[0.06] px-1.5 py-0.5 text-[11px] font-semibold text-[#9a9a9a]"
						>
							{selected[section].length}
						</span>
					</div>
					<div class="flex items-center gap-2.5">
						{#if savedSection === section}
							<span
								class="inline-flex items-center gap-1 text-[12px] font-medium text-emerald-400"
								data-testid={`saved-${section}`}
							>
								<svg
									class="h-3.5 w-3.5"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2.4"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<path d="M20 6 9 17l-5-5" />
								</svg>
								저장됨
							</span>
						{/if}
						<Button
							data-testid={`save-${section}-btn`}
							color="primary"
							size="xs"
							class="font-pretendard font-semibold"
							disabled={saving[section]}
							onclick={() => save(section)}
						>
							{saving[section] ? '저장 중...' : '저장'}
						</Button>
					</div>
				</div>

				<ol class="flex flex-col gap-2 p-4">
					{#each selected[section] as id, i (id)}
						<li
							data-testid="selected-item"
							class="flex items-center gap-3 rounded-xl border border-white/[0.06] bg-[#0f0f0f] p-2.5 pr-3"
						>
							<span
								class="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-[#FF5C16]/12 text-[11px] font-bold text-[#FF8B5C]"
							>
								{i + 1}
							</span>
							<div class="aspect-[16/10] h-10 shrink-0 overflow-hidden rounded-md bg-[#1d1d1d]">
								<img
									src={getThumbnailSrc(thumbnailOf(id))}
									alt=""
									class="h-full w-full object-cover"
								/>
							</div>
							<span class="min-w-0 flex-1 truncate text-[13.5px] font-medium">
								{titleOf(id)}
							</span>
							<div class="flex shrink-0 items-center gap-0.5">
								<button
									type="button"
									data-testid={`move-up-${section}-${i}`}
									onclick={() => moveUp(section, i)}
									aria-label="위로"
									disabled={i === 0}
									class="flex h-7 w-7 items-center justify-center rounded-lg text-[#656565] transition-colors hover:bg-white/[0.06] hover:text-white disabled:opacity-25 disabled:hover:bg-transparent"
								>
									<svg
										class="h-4 w-4"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
									>
										<path stroke-linecap="round" stroke-linejoin="round" d="m6 15 6-6 6 6" />
									</svg>
								</button>
								<button
									type="button"
									data-testid={`move-down-${section}-${i}`}
									onclick={() => moveDown(section, i)}
									aria-label="아래로"
									disabled={i === selected[section].length - 1}
									class="flex h-7 w-7 items-center justify-center rounded-lg text-[#656565] transition-colors hover:bg-white/[0.06] hover:text-white disabled:opacity-25 disabled:hover:bg-transparent"
								>
									<svg
										class="h-4 w-4"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
									>
										<path stroke-linecap="round" stroke-linejoin="round" d="m6 9 6 6 6-6" />
									</svg>
								</button>
								<button
									type="button"
									data-testid={`remove-${section}-${id}`}
									onclick={() => remove(section, id)}
									aria-label="제거"
									class="flex h-7 w-7 items-center justify-center rounded-lg text-[#656565] transition-colors hover:bg-red-500/10 hover:text-red-400"
								>
									<svg
										class="h-4 w-4"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
									>
										<path stroke-linecap="round" d="M6 6l12 12M6 18 18 6" />
									</svg>
								</button>
							</div>
						</li>
					{:else}
						<li
							class="rounded-xl border border-dashed border-white/[0.08] py-8 text-center text-[13px] text-[#656565]"
							data-testid={`empty-${section}`}
						>
							아래 후보에서 렉처를 추가하세요
						</li>
					{/each}
				</ol>
			</section>
		{/each}
	</div>

	<!-- 후보 -->
	<section class="flex flex-col gap-4">
		<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
			<h2 class="text-[16px] font-bold tracking-[-0.01em]">후보 렉처</h2>
			<div class="relative sm:w-72">
				<svg
					class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#656565]"
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
					data-testid="candidate-search-input"
					bind:value={search}
					placeholder="후보 검색"
					class="w-full rounded-xl border border-white/[0.08] bg-[#141414] py-2 pl-9 pr-3 text-[13.5px] text-white placeholder:text-[#656565] outline-none transition-colors focus:border-[#FF5C16]"
				/>
			</div>
		</div>

		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each filteredCandidates as lecture (lecture.id)}
				<div
					data-testid={`candidate-${lecture.id}`}
					class="group flex flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414] transition-all duration-200 hover:-translate-y-0.5 hover:border-[#FF5C16]/40 hover:bg-[#171717]"
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
					<div class="flex flex-1 flex-col gap-3 p-4">
						<div class="flex flex-col gap-2">
							<h3 class="line-clamp-2 text-[15px] font-bold leading-snug tracking-[-0.01em]">
								{lecture.title}
							</h3>
							{#if tagLabels(lecture.tags).length}
								<div class="flex flex-wrap items-center gap-1.5">
									{#each tagLabels(lecture.tags).slice(0, 2) as tag (tag)}
										<span
											class="inline-flex items-center rounded-md bg-white/[0.05] px-2 py-0.5 text-[11px] font-medium text-[#9a9a9a]"
										>
											{tag}
										</span>
									{/each}
								</div>
							{/if}
						</div>
						<div class="mt-auto flex items-center gap-2">
							{#each sections as section (section)}
								{@const isAdded = selected[section].includes(lecture.id)}
								<button
									type="button"
									data-testid={`add-to-${section}-${lecture.id}`}
									onclick={() => add(section, lecture.id)}
									aria-pressed={isAdded}
									class="flex flex-1 items-center justify-center gap-1.5 rounded-xl border px-3 py-2 text-[13px] font-semibold transition-colors
										{isAdded
										? 'border-emerald-500/40 bg-emerald-500/12 text-emerald-300'
										: 'border-[#FF5C16]/35 bg-[#FF5C16]/10 text-[#FF8B5C] hover:border-[#FF5C16]/70 hover:bg-[#FF5C16]/20 hover:text-white'}"
								>
									{#if isAdded}
										<svg
											class="h-3.5 w-3.5"
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="2.4"
											stroke-linecap="round"
											stroke-linejoin="round"
										>
											<path d="M20 6 9 17l-5-5" />
										</svg>
									{:else}
										<svg
											class="h-3.5 w-3.5"
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="2.4"
											stroke-linecap="round"
											stroke-linejoin="round"
										>
											<path d="M12 5v14M5 12h14" />
										</svg>
									{/if}
									{sectionTag[section]}
								</button>
							{/each}
						</div>
					</div>
				</div>
			{:else}
				<div
					class="col-span-full flex flex-col items-center gap-1.5 rounded-2xl border border-dashed border-white/[0.1] bg-[#101010] py-12 text-center"
					data-testid="candidates-empty"
				>
					<p class="text-[14px] font-semibold text-white">
						{search.trim() ? '검색 결과가 없습니다' : '후보 렉처가 없습니다'}
					</p>
					<p class="text-[12px] text-[#656565]">
						{search.trim() ? '다른 키워드로 검색해 보세요' : '렉처 탭에서 먼저 렉처를 만드세요'}
					</p>
				</div>
			{/each}
		</div>
	</section>
</div>
