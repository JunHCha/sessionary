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

	const sections: CurationSection[] = ['TRENDING', 'NEW']
	const sectionLabel: Record<CurationSection, string> = {
		TRENDING: '요즘 많이 보는 렉처',
		NEW: '새로운 렉처'
	}

	let candidates = $state<LectureInList[]>([])
	let selected = $state<Record<CurationSection, number[]>>({ TRENDING: [], NEW: [] })
	let saving = $state<Record<CurationSection, boolean>>({ TRENDING: false, NEW: false })
	let savedSection = $state<CurationSection | null>(null)
	let error = $state('')

	const candidateMap = $derived(new Map(candidates.map((c) => [c.id, c])))

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

<div class="flex flex-col gap-8">
	<h1 class="text-2xl font-bold">홈 큐레이션</h1>

	{#if error}
		<p class="text-red-400 text-sm" data-testid="curation-error">{error}</p>
	{/if}

	<div class="grid gap-8 md:grid-cols-2">
		{#each sections as section (section)}
			<section
				data-testid={`section-${section}`}
				class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]"
			>
				<div class="flex items-center justify-between">
					<h2 class="text-lg font-semibold">{sectionLabel[section]}</h2>
					<div class="flex items-center gap-2">
						{#if savedSection === section}
							<span class="text-green-400 text-xs" data-testid={`saved-${section}`}
								>저장됨</span
							>
						{/if}
						<Button
							data-testid={`save-${section}-btn`}
							color="primary"
							size="xs"
							disabled={saving[section]}
							onclick={() => save(section)}
						>
							{saving[section] ? '저장 중...' : '저장'}
						</Button>
					</div>
				</div>

				<ol class="flex flex-col gap-2">
					{#each selected[section] as id, i (id)}
						<li
							data-testid="selected-item"
							class="flex items-center justify-between px-3 py-2 rounded bg-black border border-[#333]"
						>
							<span class="text-sm">{i + 1}. {titleOf(id)}</span>
							<div class="flex items-center gap-1">
								<button
									type="button"
									data-testid={`move-up-${section}-${i}`}
									onclick={() => moveUp(section, i)}
									class="text-xs px-1 text-[#888] hover:text-white"
								>
									▲
								</button>
								<button
									type="button"
									data-testid={`move-down-${section}-${i}`}
									onclick={() => moveDown(section, i)}
									class="text-xs px-1 text-[#888] hover:text-white"
								>
									▼
								</button>
								<button
									type="button"
									data-testid={`remove-${section}-${id}`}
									onclick={() => remove(section, id)}
									class="text-xs px-1 text-[#888] hover:text-red-400"
								>
									✕
								</button>
							</div>
						</li>
					{:else}
						<li class="text-sm text-[#888]" data-testid={`empty-${section}`}>
							비어 있음
						</li>
					{/each}
				</ol>
			</section>
		{/each}
	</div>

	<section class="flex flex-col gap-2">
		<h2 class="text-lg font-semibold">후보 렉처</h2>
		<div class="flex flex-col gap-2">
			{#each candidates as lecture (lecture.id)}
				<div
					data-testid={`candidate-${lecture.id}`}
					class="flex items-center justify-between px-4 py-3 rounded bg-[#141414] border border-[#262626]"
				>
					<span class="text-sm"
						>{lecture.title} <span class="text-[#888]">#{lecture.id}</span></span
					>
					<div class="flex items-center gap-2">
						{#each sections as section (section)}
							<Button
								data-testid={`add-to-${section}-${lecture.id}`}
								color="alternative"
								size="xs"
								onclick={() => add(section, lecture.id)}
							>
								{section === 'TRENDING' ? '인기' : '신규'}에 추가
							</Button>
						{/each}
					</div>
				</div>
			{/each}
		</div>
	</section>
</div>
