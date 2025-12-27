<script lang="ts">
	import { page } from '$app/stores'
	import { getLectureLectureLectureIdGet } from '$lib/api'
	import type { LectureDetail } from '$lib/api'
	import { LectureInfo, SessionList, SheetPreview } from '$lib/features/lecture'

	let lecture = $state<LectureDetail | null>(null)
	let currentSessionIndex = $state(1)
	let isLoading = $state(true)

	async function fetchLecture(id: number) {
		try {
			isLoading = true
			const response = await getLectureLectureLectureIdGet({ lectureId: id })
			lecture = response.data
		} catch (error) {
			console.error('Failed to fetch lecture:', error)
		} finally {
			isLoading = false
		}
	}

	$effect(() => {
		const id = Number($page.params.id)
		if (id) {
			fetchLecture(id)
		}
	})
</script>

<main class="min-h-screen pt-24 px-20">
	{#if isLoading}
		<div class="flex items-center justify-center h-[60vh]">
			<div
				class="w-12 h-12 border-4 border-brand-primary border-t-transparent rounded-full animate-spin"
			></div>
		</div>
	{:else if lecture}
		<div class="flex gap-12">
			<section class="w-[45%] flex flex-col gap-8">
				<LectureInfo {lecture} />
				<SheetPreview />
			</section>

			<section class="w-[55%]">
				<SessionList sessions={lecture.lessons} {currentSessionIndex} />
			</section>
		</div>
	{:else}
		<div class="flex items-center justify-center h-[60vh]">
			<p class="text-content-secondary text-xl">렉처를 찾을 수 없습니다.</p>
		</div>
	{/if}
</main>
