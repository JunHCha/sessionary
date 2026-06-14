<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { page } from '$app/stores'
	import { Button } from 'flowbite-svelte'
	import { waitForApiInit, createLessonLessonPost } from '$lib/api'
	import type { SessionType } from '$lib/api'
	import { setLessonDraft } from '$lib/features/admin/stores/lesson-draft.svelte'

	const sessionTypes: SessionType[] = ['PLAY', 'TALK', 'JAM', 'BASIC', 'SHEET']

	let lectureId = $state(0)
	let title = $state('')
	let sessionType = $state<SessionType>('PLAY')
	let lectureOrdering = $state(0)
	let lengthSec = $state(0)
	let text = $state('')
	let saving = $state(false)
	let error = $state('')

	onMount(async () => {
		await waitForApiInit()
		lectureId = Number($page.url.searchParams.get('lectureId') ?? '0')
	})

	async function create() {
		if (!title.trim()) return
		saving = true
		error = ''
		try {
			const res = await createLessonLessonPost({
				requestBody: {
					lecture_id: lectureId,
					title: title.trim(),
					session_type: sessionType,
					lecture_ordering: lectureOrdering,
					length_sec: lengthSec,
					text
				}
			})
			setLessonDraft(res.data)
			goto(`/admin/lessons/${res.data.id}`)
		} catch (e) {
			error = '레슨 생성에 실패했습니다'
			console.error(e)
		} finally {
			saving = false
		}
	}
</script>

<div class="flex flex-col gap-7 font-pretendard">
	<header class="flex flex-col gap-3">
		<a
			href={`/admin/lectures/${lectureId}`}
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
			렉처로 돌아가기
		</a>
		<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
			New Lesson
		</span>
		<h1 class="text-[26px] font-bold leading-tight tracking-[-0.02em] sm:text-[30px]">
			새 레슨
		</h1>
	</header>

	<section
		class="mx-auto w-full max-w-[680px] overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414]"
	>
		<div class="border-b border-white/[0.06] px-5 py-4">
			<h2 class="text-[15px] font-bold tracking-[-0.01em]">기본 정보</h2>
		</div>
		<div class="flex flex-col gap-4 p-5">
			<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
				제목
				<input
					data-testid="lesson-title-input"
					bind:value={title}
					placeholder="레슨 제목"
					class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white placeholder:text-[#5a5a5a] outline-none transition-colors focus:border-[#FF5C16]"
				/>
			</label>
			<div class="grid gap-3 sm:grid-cols-[1.5fr_1fr_1fr]">
				<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
					세션 타입
					<select
						data-testid="lesson-session-type"
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
						data-testid="lesson-ordering-input"
						bind:value={lectureOrdering}
						class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
					/>
				</label>
				<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
					길이(초)
					<input
						type="number"
						data-testid="lesson-length-input"
						bind:value={lengthSec}
						class="rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white outline-none transition-colors focus:border-[#FF5C16]"
					/>
				</label>
			</div>
			<label class="flex flex-col gap-1.5 text-[13px] font-medium text-[#bdbdbd]">
				설명
				<textarea
					data-testid="lesson-text-input"
					bind:value={text}
					rows="3"
					placeholder="레슨 설명 (선택)"
					class="resize-none rounded-xl border border-white/[0.1] bg-[#0d0d0d] px-3.5 py-2.5 text-[14px] text-white placeholder:text-[#5a5a5a] outline-none transition-colors focus:border-[#FF5C16]"
				></textarea>
			</label>
			<div class="flex items-center gap-3 border-t border-white/[0.06] pt-4">
				<Button
					data-testid="create-lesson-btn"
					color="primary"
					class="font-pretendard font-semibold"
					disabled={saving}
					onclick={create}
				>
					{saving ? '생성 중...' : '레슨 생성'}
				</Button>
				<span class="text-[12.5px] text-[#656565]">생성 후 편집 화면으로 이동합니다</span>
				{#if error}
					<span
						class="text-[13px] font-medium text-red-400"
						data-testid="lesson-create-error"
					>
						{error}
					</span>
				{/if}
			</div>
		</div>
	</section>
</div>
