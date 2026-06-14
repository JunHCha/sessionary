<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import {
		waitForApiInit,
		getLectureLectureLectureIdGet,
		updateLectureLectureLectureIdPatch
	} from '$lib/api'
	import type { LectureDetail, LessonInLecture } from '$lib/api'

	let { data }: { data: { lectureId: number } } = $props()

	const lectureType = ['원곡카피', '해석버전', '기본기']
	const difficultyLevel = ['Easy', 'Intermediate', 'Advanced']

	let lecture = $state<LectureDetail | null>(null)
	let title = $state('')
	let description = $state('')
	let thumbnail = $state('')
	let typeTag = $state('원곡카피')
	let difficultyTag = $state('Easy')
	let lessons = $state<LessonInLecture[]>([])
	let loading = $state(true)
	let saving = $state(false)
	let saved = $state(false)
	let error = $state('')

	onMount(async () => {
		await waitForApiInit()
		try {
			const res = await getLectureLectureLectureIdGet({ lectureId: data.lectureId })
			applyDetail(res.data)
		} catch (e) {
			error = '렉처를 불러오지 못했습니다'
			console.error(e)
		} finally {
			loading = false
		}
	})

	function applyDetail(detail: LectureDetail) {
		lecture = detail
		title = detail.title
		description = detail.description
		thumbnail = detail.thumbnail ?? ''
		lessons = detail.lessons
		const tags = (detail.tags ?? []) as string[]
		if (tags[0]) typeTag = tags[0]
		if (tags[1]) difficultyTag = tags[1]
	}

	async function save() {
		saving = true
		saved = false
		error = ''
		try {
			const res = await updateLectureLectureLectureIdPatch({
				lectureId: data.lectureId,
				requestBody: {
					title: title.trim(),
					description: description.trim(),
					thumbnail: thumbnail.trim() || null,
					tags: [typeTag, difficultyTag]
				}
			})
			applyDetail(res.data)
			saved = true
		} catch (e) {
			error = '저장에 실패했습니다'
			console.error(e)
		} finally {
			saving = false
		}
	}
</script>

<div class="flex flex-col gap-8">
	<div class="flex items-center gap-3">
		<a href="/admin/lectures" class="text-sm text-[#888] hover:text-[#FF5C16]">← 목록</a>
		<h1 class="text-2xl font-bold">렉처 편집 #{data.lectureId}</h1>
	</div>

	{#if loading}
		<p class="text-[#888]" data-testid="lecture-edit-loading">불러오는 중...</p>
	{:else if lecture}
		<section class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]">
			<label class="flex flex-col gap-1 text-sm">
				제목
				<input
					data-testid="edit-title-input"
					bind:value={title}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				/>
			</label>
			<label class="flex flex-col gap-1 text-sm">
				설명
				<textarea
					data-testid="edit-desc-input"
					bind:value={description}
					rows="3"
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				></textarea>
			</label>
			<label class="flex flex-col gap-1 text-sm">
				썸네일 URL
				<input
					data-testid="edit-thumbnail-input"
					bind:value={thumbnail}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				/>
			</label>
			<div class="flex gap-3">
				<label class="flex flex-col gap-1 text-sm flex-1">
					유형
					<select
						data-testid="edit-type-select"
						bind:value={typeTag}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					>
						{#each lectureType as t (t)}
							<option value={t}>{t}</option>
						{/each}
					</select>
				</label>
				<label class="flex flex-col gap-1 text-sm flex-1">
					난이도
					<select
						data-testid="edit-difficulty-select"
						bind:value={difficultyTag}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					>
						{#each difficultyLevel as d (d)}
							<option value={d}>{d}</option>
						{/each}
					</select>
				</label>
			</div>
			<div class="flex items-center gap-3">
				<Button
					data-testid="save-lecture-btn"
					color="primary"
					disabled={saving}
					onclick={save}
				>
					{saving ? '저장 중...' : '저장'}
				</Button>
				{#if saved}
					<span class="text-green-400 text-sm" data-testid="save-status">저장됨</span>
				{/if}
				{#if error}
					<span class="text-red-400 text-sm" data-testid="save-status">{error}</span>
				{/if}
			</div>
		</section>

		<section class="flex flex-col gap-2">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-semibold">레슨</h2>
				<a
					href={`/admin/lessons/new?lectureId=${data.lectureId}`}
					data-testid="add-lesson-link"
					class="text-sm text-[#FF5C16] hover:underline"
				>
					+ 레슨 추가
				</a>
			</div>
			{#each lessons as lesson (lesson.id)}
				<a
					href={`/admin/lessons/${lesson.id}`}
					data-testid="lesson-item"
					class="flex items-center justify-between px-4 py-3 rounded bg-[#141414] border border-[#262626] hover:border-[#FF5C16] transition-colors"
				>
					<span>{lesson.title}</span>
					<span class="text-xs text-[#888]">#{lesson.id}</span>
				</a>
			{:else}
				<p class="text-sm text-[#888]" data-testid="no-lessons">아직 레슨이 없습니다</p>
			{/each}
		</section>
	{/if}
</div>
