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

<div class="flex flex-col gap-7 font-pretendard" data-testid="lesson-editor">
	<header class="flex flex-col gap-3">
		<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
			Lesson #{data.lessonId}
		</span>
		<h1 class="text-[26px] font-bold leading-tight tracking-[-0.02em] sm:text-[30px]">
			{ready && title ? title : '레슨 편집'}
		</h1>
	</header>

	{#if ready}
		<!-- 기본 정보 -->
		<section class="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]">
			<div class="flex items-center gap-2.5 border-b border-white/[0.06] px-5 py-4">
				<span class="text-[11px] font-bold text-[#FF5C16]">01</span>
				<h2 class="text-[15px] font-bold tracking-[-0.01em]">기본 정보</h2>
			</div>
			<div class="flex flex-col gap-4 p-5">
				<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
					제목
					<input
						data-testid="lesson-edit-title"
						bind:value={title}
						class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
					/>
				</label>
				<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						세션 타입
						<select
							data-testid="lesson-edit-session-type"
							bind:value={sessionType}
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						>
							{#each sessionTypes as t (t)}
								<option value={t}>{t}</option>
							{/each}
						</select>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						순서
						<input
							type="number"
							bind:value={lectureOrdering}
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						길이(초)
						<input
							type="number"
							bind:value={lengthSec}
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
					<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
						싱크 오프셋
						<input
							type="number"
							bind:value={syncOffset}
							class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
					</label>
				</div>
				<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
					설명
					<textarea
						bind:value={text}
						rows="2"
						class="resize-none rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
					></textarea>
				</label>
			</div>
		</section>

		<!-- 미디어 -->
		<section class="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]">
			<div class="flex items-center gap-2.5 border-b border-white/[0.06] px-5 py-4">
				<span class="text-[11px] font-bold text-[#FF5C16]">02</span>
				<h2 class="text-[15px] font-bold tracking-[-0.01em]">미디어 업로드</h2>
			</div>
			<div class="grid gap-4 p-5 sm:grid-cols-2">
				<div
					class="flex flex-col gap-3 rounded-xl border border-white/[0.06] bg-[#0f0f0f] p-4"
				>
					<FileUploadField
						label="동영상"
						accept="video/*,.mp4,.m3u8"
						testidPrefix="video-upload"
						onUpload={uploadVideo}
					/>
					{#if videoUrl}
						<p
							class="truncate rounded-lg bg-white/[0.04] px-2.5 py-1.5 text-[11px] text-[#9a9a9a]"
							data-testid="video-url"
							title={videoUrl}
						>
							현재: {videoUrl}
						</p>
					{/if}
				</div>
				<div
					class="flex flex-col gap-3 rounded-xl border border-white/[0.06] bg-[#0f0f0f] p-4"
				>
					<FileUploadField
						label="악보"
						accept=".musicxml,.xml,.mxl,.pdf"
						testidPrefix="sheetmusic-upload"
						onUpload={uploadSheetmusic}
					/>
					{#if sheetmusicUrl}
						<p
							class="truncate rounded-lg bg-white/[0.04] px-2.5 py-1.5 text-[11px] text-[#9a9a9a]"
							data-testid="sheetmusic-url"
							title={sheetmusicUrl}
						>
							현재: {sheetmusicUrl}
						</p>
					{/if}
				</div>
			</div>
		</section>

		<!-- 자막 -->
		<section class="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]">
			<div class="flex items-center gap-2.5 border-b border-white/[0.06] px-5 py-4">
				<span class="text-[11px] font-bold text-[#FF5C16]">03</span>
				<h2 class="text-[15px] font-bold tracking-[-0.01em]">자막</h2>
			</div>
			<div class="p-5">
				<SubtitleEditor bind:rows={subtitles} />
			</div>
		</section>

		<!-- 저장 바 -->
		<div
			class="sticky bottom-0 -mx-5 flex items-center gap-3 border-t border-white/[0.06] bg-[#0C0C0C]/95 px-5 py-4 backdrop-blur sm:-mx-8 sm:px-8 lg:-mx-12 lg:px-12"
		>
			<Button
				data-testid="save-lesson-btn"
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
					data-testid="lesson-save-status"
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
				<span class="text-[13px] font-medium text-red-400" data-testid="lesson-save-status">
					{error}
				</span>
			{/if}
		</div>
	{/if}
</div>
