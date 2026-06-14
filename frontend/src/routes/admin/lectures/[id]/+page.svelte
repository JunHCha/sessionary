<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import {
		waitForApiInit,
		getLectureLectureLectureIdGet,
		updateLectureLectureLectureIdPatch
	} from '$lib/api'
	import type { LectureDetail, LessonInLecture } from '$lib/api'
	import { getThumbnailSrc } from '$lib/features/lecture/utils/format'

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

<div class="flex flex-col gap-7 font-pretendard">
	<header class="flex flex-col gap-3">
		<a
			href="/admin/lectures"
			class="inline-flex w-fit items-center gap-1.5 text-[13px] font-medium text-[#848484] transition-colors hover:text-[#FF5C16]"
		>
			<svg
				class="h-4 w-4"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.8"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M19 12H5M11 6l-6 6 6 6" />
			</svg>
			렉처 목록
		</a>
		<div class="flex items-center gap-3">
			<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
				Lecture #{data.lectureId}
			</span>
		</div>
		<h1 class="text-[26px] font-bold leading-tight tracking-[-0.02em] sm:text-[30px]">
			{loading ? '렉처 편집' : title || '렉처 편집'}
		</h1>
	</header>

	{#if loading}
		<div class="flex items-center gap-3 text-[#848484]" data-testid="lecture-edit-loading">
			<span
				class="h-4 w-4 animate-spin rounded-full border-2 border-white/20 border-t-[#FF5C16]"
			></span>
			<span class="text-[14px]">불러오는 중...</span>
		</div>
	{:else if lecture}
		<div class="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
			<!-- 좌: 속성 -->
			<section
				class="flex flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]"
			>
				<div class="border-b border-white/[0.06] px-5 py-4">
					<h2 class="text-[15px] font-bold tracking-[-0.01em]">속성</h2>
				</div>
				<div class="flex flex-col gap-4 p-5">
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						제목
						<input
							data-testid="edit-title-input"
							bind:value={title}
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						설명
						<textarea
							data-testid="edit-desc-input"
							bind:value={description}
							rows="3"
							class="resize-none rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						></textarea>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						썸네일 URL
						<input
							data-testid="edit-thumbnail-input"
							bind:value={thumbnail}
							placeholder="https://..."
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white placeholder:text-[#5a5a5a] outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>

					<!-- 썸네일 미리보기 -->
					<div class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						미리보기
						<div
							class="relative aspect-[16/9] w-full max-w-[280px] overflow-hidden rounded-xl border border-white/[0.08] bg-[#1d1d1d]"
						>
							<img
								src={getThumbnailSrc(thumbnail || null)}
								alt="썸네일 미리보기"
								class="h-full w-full object-cover"
							/>
						</div>
					</div>

					<div class="grid grid-cols-2 gap-3">
						<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
							유형
							<select
								data-testid="edit-type-select"
								bind:value={typeTag}
								class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
							>
								{#each lectureType as t (t)}
									<option value={t}>{t}</option>
								{/each}
							</select>
						</label>
						<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
							난이도
							<select
								data-testid="edit-difficulty-select"
								bind:value={difficultyTag}
								class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
							>
								{#each difficultyLevel as d (d)}
									<option value={d}>{d}</option>
								{/each}
							</select>
						</label>
					</div>

					<div class="flex items-center gap-3 border-t border-white/[0.06] pt-4">
						<Button
							data-testid="save-lecture-btn"
							color="primary"
							class="font-pretendard font-semibold"
							disabled={saving}
							onclick={save}
						>
							{saving ? '저장 중...' : '저장'}
						</Button>
						{#if saved}
							<span
								class="inline-flex items-center gap-1.5 text-[13px] font-medium text-emerald-400"
								data-testid="save-status"
							>
								<svg
									class="h-4 w-4"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2.2"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<path d="M20 6 9 17l-5-5" />
								</svg>
								저장됨
							</span>
						{/if}
						{#if error}
							<span
								class="text-[13px] font-medium text-red-400"
								data-testid="save-status"
							>
								{error}
							</span>
						{/if}
					</div>
				</div>
			</section>

			<!-- 우: 레슨 -->
			<section
				class="flex h-fit flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]"
			>
				<div
					class="flex items-center justify-between border-b border-white/[0.06] px-5 py-4"
				>
					<div class="flex items-center gap-2">
						<h2 class="text-[15px] font-bold tracking-[-0.01em]">레슨</h2>
						<span
							class="rounded-md bg-white/[0.06] px-2 py-0.5 text-[11px] font-semibold text-[#9a9a9a]"
						>
							{lessons.length}
						</span>
					</div>
					<a
						href={`/admin/lessons/new?lectureId=${data.lectureId}`}
						data-testid="add-lesson-link"
						class="inline-flex items-center gap-1 text-[13px] font-semibold text-[#FF5C16] transition-colors hover:text-[#FF8B5C]"
					>
						<svg
							class="h-4 w-4"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2.2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path d="M12 5v14M5 12h14" />
						</svg>
						레슨 추가
					</a>
				</div>
				<div class="flex flex-col gap-2 p-4">
					{#each lessons as lesson (lesson.id)}
						<a
							href={`/admin/lessons/${lesson.id}`}
							data-testid="lesson-item"
							class="group flex items-center justify-between rounded-xl border border-white/[0.06] bg-[#0f0f0f] px-4 py-3 transition-colors hover:border-[#FF5C16]/40 hover:bg-[#141414]"
						>
							<span
								class="text-[14px] font-medium transition-colors group-hover:text-[#FF5C16]"
							>
								{lesson.title}
							</span>
							<span class="text-[11px] font-medium text-[#656565]">#{lesson.id}</span>
						</a>
					{:else}
						<div
							class="flex flex-col items-center gap-1.5 rounded-xl border border-dashed border-white/[0.08] py-10 text-center"
							data-testid="no-lessons"
						>
							<p class="text-[14px] font-medium text-[#9a9a9a]">
								아직 레슨이 없습니다
							</p>
							<p class="text-[12px] text-[#656565]">
								'레슨 추가'로 첫 레슨을 만드세요
							</p>
						</div>
					{/each}
				</div>
			</section>
		</div>
	{/if}
</div>
