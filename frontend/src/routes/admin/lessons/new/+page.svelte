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

<div class="flex flex-col gap-6">
	<div class="flex items-center gap-3">
		<a href={`/admin/lectures/${lectureId}`} class="text-sm text-[#888] hover:text-[#FF5C16]"
			>← 렉처</a
		>
		<h1 class="text-2xl font-bold">새 레슨</h1>
	</div>

	<section class="flex flex-col gap-3 p-4 rounded-lg bg-[#141414] border border-[#262626]">
		<label class="flex flex-col gap-1 text-sm">
			제목
			<input
				data-testid="lesson-title-input"
				bind:value={title}
				class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
			/>
		</label>
		<div class="flex gap-3">
			<label class="flex flex-col gap-1 text-sm flex-1">
				세션 타입
				<select
					data-testid="lesson-session-type"
					bind:value={sessionType}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				>
					{#each sessionTypes as t (t)}
						<option value={t}>{t}</option>
					{/each}
				</select>
			</label>
			<label class="flex flex-col gap-1 text-sm w-32">
				순서
				<input
					type="number"
					data-testid="lesson-ordering-input"
					bind:value={lectureOrdering}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				/>
			</label>
			<label class="flex flex-col gap-1 text-sm w-32">
				길이(초)
				<input
					type="number"
					data-testid="lesson-length-input"
					bind:value={lengthSec}
					class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
				/>
			</label>
		</div>
		<label class="flex flex-col gap-1 text-sm">
			설명
			<textarea
				data-testid="lesson-text-input"
				bind:value={text}
				rows="2"
				class="bg-black border border-[#333] rounded px-3 py-2 focus:border-[#FF5C16] outline-none"
			></textarea>
		</label>
		<div class="flex items-center gap-3">
			<Button
				data-testid="create-lesson-btn"
				color="primary"
				disabled={saving}
				onclick={create}
			>
				{saving ? '생성 중...' : '레슨 생성'}
			</Button>
			{#if error}
				<span class="text-red-400 text-sm" data-testid="lesson-create-error">{error}</span>
			{/if}
		</div>
	</section>
</div>
