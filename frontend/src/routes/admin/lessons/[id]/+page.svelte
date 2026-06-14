<script lang="ts">
	import { onMount } from 'svelte'
	import { Button } from 'flowbite-svelte'
	import {
		waitForApiInit,
		updateLessonLessonLessonIdPatch,
		uploadLessonVideoLessonLessonIdVideoPost,
		uploadLessonSheetmusicLessonLessonIdSheetmusicPost
	} from '$lib/api'
	import type { LessonAdminDetail, SessionType } from '$lib/api'
	import SubtitleEditor from '$lib/features/admin/components/SubtitleEditor.svelte'
	import FileUploadField from '$lib/features/admin/components/FileUploadField.svelte'
	import type { SubtitleRow } from '$lib/features/admin/utils/subtitle-parser'
	import { takeLessonDraft } from '$lib/features/admin/stores/lesson-draft.svelte'

	let { data }: { data: { lessonId: number } } = $props()

	const sessionTypes: SessionType[] = ['PLAY', 'TALK', 'JAM', 'BASIC', 'SHEET']

	let ready = $state(false)
	let title = $state('')
	let sessionType = $state<SessionType>('PLAY')
	let lectureOrdering = $state(0)
	let lengthSec = $state(0)
	let text = $state('')
	let syncOffset = $state(0)
	let videoUrl = $state<string | null>(null)
	let sheetmusicUrl = $state<string | null>(null)
	let subtitles = $state<SubtitleRow[]>([])
	let saving = $state(false)
	let saved = $state(false)
	let error = $state('')

	onMount(async () => {
		await waitForApiInit()
		const draft = takeLessonDraft(data.lessonId)
		if (draft) {
			applyDraft(draft)
		}
		ready = true
	})

	function applyDraft(lesson: LessonAdminDetail) {
		title = lesson.title
		sessionType = lesson.session_type ?? 'PLAY'
		lectureOrdering = lesson.lecture_ordering
		lengthSec = lesson.length_sec
		text = lesson.text ?? ''
		syncOffset = lesson.sync_offset
		videoUrl = lesson.video_url
		sheetmusicUrl = lesson.sheetmusic_url
		subtitles = lesson.subtitles ?? []
	}

	async function save() {
		saving = true
		saved = false
		error = ''
		try {
			const res = await updateLessonLessonLessonIdPatch({
				lessonId: data.lessonId,
				requestBody: {
					title: title.trim(),
					session_type: sessionType,
					lecture_ordering: lectureOrdering,
					length_sec: lengthSec,
					text,
					sync_offset: syncOffset,
					subtitles
				}
			})
			applyDraft(res.data)
			saved = true
		} catch (e) {
			error = '저장에 실패했습니다'
			console.error(e)
		} finally {
			saving = false
		}
	}

	async function uploadVideo(file: File) {
		const res = await uploadLessonVideoLessonLessonIdVideoPost({
			lessonId: data.lessonId,
			formData: { file }
		})
		videoUrl = res.data.video_url
	}

	async function uploadSheetmusic(file: File) {
		const res = await uploadLessonSheetmusicLessonLessonIdSheetmusicPost({
			lessonId: data.lessonId,
			formData: { file }
		})
		sheetmusicUrl = res.data.sheetmusic_url
	}
</script>

<div class="flex flex-col gap-6" data-testid="lesson-editor">
	<h1 class="text-2xl font-bold">레슨 편집 #{data.lessonId}</h1>

	{#if ready}
		<section class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]">
			<label class="flex flex-col gap-1 text-sm">
				제목
				<input
					data-testid="lesson-edit-title"
					bind:value={title}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				/>
			</label>
			<div class="flex gap-3 flex-wrap">
				<label class="flex flex-col gap-1 text-sm flex-1 min-w-[120px]">
					세션 타입
					<select
						data-testid="lesson-edit-session-type"
						bind:value={sessionType}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					>
						{#each sessionTypes as t (t)}
							<option value={t}>{t}</option>
						{/each}
					</select>
				</label>
				<label class="flex flex-col gap-1 text-sm w-28">
					순서
					<input
						type="number"
						bind:value={lectureOrdering}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					/>
				</label>
				<label class="flex flex-col gap-1 text-sm w-28">
					길이(초)
					<input
						type="number"
						bind:value={lengthSec}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					/>
				</label>
				<label class="flex flex-col gap-1 text-sm w-28">
					싱크 오프셋
					<input
						type="number"
						bind:value={syncOffset}
						class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
					/>
				</label>
			</div>
		</section>

		<section class="flex flex-col gap-4 p-4 rounded-lg bg-[#141414] border border-[#262626]">
			<h2 class="text-lg font-semibold">미디어</h2>
			<FileUploadField
				label="동영상"
				accept="video/*,.mp4,.m3u8"
				testidPrefix="video-upload"
				onUpload={uploadVideo}
			/>
			{#if videoUrl}
				<p class="text-xs text-[#888]" data-testid="video-url">현재: {videoUrl}</p>
			{/if}
			<FileUploadField
				label="악보"
				accept=".musicxml,.xml,.mxl,.pdf"
				testidPrefix="sheetmusic-upload"
				onUpload={uploadSheetmusic}
			/>
			{#if sheetmusicUrl}
				<p class="text-xs text-[#888]" data-testid="sheetmusic-url">
					현재: {sheetmusicUrl}
				</p>
			{/if}
		</section>

		<section class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]">
			<h2 class="text-lg font-semibold">자막</h2>
			<SubtitleEditor bind:rows={subtitles} />
		</section>

		<div class="flex items-center gap-3">
			<Button data-testid="save-lesson-btn" color="primary" disabled={saving} onclick={save}>
				{saving ? '저장 중...' : '저장'}
			</Button>
			{#if saved}
				<span class="text-green-400 text-sm" data-testid="lesson-save-status">저장됨</span>
			{/if}
			{#if error}
				<span class="text-red-400 text-sm" data-testid="lesson-save-status">{error}</span>
			{/if}
		</div>
	{/if}
</div>
