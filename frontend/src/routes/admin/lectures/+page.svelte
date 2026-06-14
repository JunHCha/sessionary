<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import { waitForApiInit, getLecturesLectureGet, createLectureLecturePost } from '$lib/api'
	import type { LectureInList } from '$lib/api'

	let lectures = $state<LectureInList[]>([])
	let title = $state('')
	let description = $state('')
	let creating = $state(false)
	let error = $state('')

	onMount(async () => {
		await waitForApiInit()
		await loadLectures()
	})

	async function loadLectures() {
		try {
			const res = await getLecturesLectureGet({})
			lectures = res.data ?? []
		} catch (e) {
			error = '렉처 목록을 불러오지 못했습니다'
			console.error(e)
		}
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
			title = ''
			description = ''
		} catch (e) {
			error = '렉처 생성에 실패했습니다'
			console.error(e)
		} finally {
			creating = false
		}
	}
</script>

<div class="flex flex-col gap-8">
	<h1 class="text-2xl font-bold">렉처 관리</h1>

	<section class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]">
		<h2 class="text-lg font-semibold">새 렉처</h2>
		<input
			data-testid="lecture-title-input"
			bind:value={title}
			placeholder="제목"
			class="bg-black border border-[#333] rounded px-3 py-2 text-sm focus:border-[#FF5C16] outline-none"
		/>
		<textarea
			data-testid="lecture-desc-input"
			bind:value={description}
			placeholder="설명"
			rows="2"
			class="bg-black border border-[#333] rounded px-3 py-2 text-sm focus:border-[#FF5C16] outline-none"
		></textarea>
		<div>
			<Button
				data-testid="create-lecture-btn"
				color="primary"
				disabled={creating}
				onclick={createLecture}
			>
				{creating ? '생성 중...' : '렉처 생성'}
			</Button>
		</div>
	</section>

	{#if error}
		<p class="text-red-400 text-sm" data-testid="lecture-error">{error}</p>
	{/if}

	<section class="flex flex-col gap-2">
		<h2 class="text-lg font-semibold">렉처 목록</h2>
		{#each lectures as lecture (lecture.id)}
			<a
				href={`/admin/lectures/${lecture.id}`}
				data-testid="lecture-row"
				class="flex items-center justify-between px-4 py-3 rounded bg-[#141414] border border-[#262626] hover:border-[#FF5C16] transition-colors"
			>
				<span class="font-medium">{lecture.title}</span>
				<span class="text-xs text-[#888]">#{lecture.id}</span>
			</a>
		{/each}
	</section>
</div>
