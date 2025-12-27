<script lang="ts">
	import type { LectureDetail } from '$lib/api'
	import { formatDuration, getThumbnailSrc } from '../utils/format'

	let { lecture }: { lecture: LectureDetail } = $props()

	let totalDuration = $derived(
		lecture.lessons.reduce((acc, lesson) => acc + lesson.length_sec, 0)
	)
</script>

<div class="flex flex-col gap-6">
	<div
		class="relative w-full aspect-video rounded-2xl overflow-hidden shadow-[0_4px_32px_rgba(255,92,22,0.15)]"
	>
		<img src={getThumbnailSrc(null)} alt={lecture.title} class="w-full h-full object-cover" />
		<div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
	</div>

	<div class="flex flex-col gap-4">
		<h1 class="text-4xl font-pretendard font-bold text-white leading-tight">
			{lecture.title}
		</h1>

		{#if lecture.artist}
			<p class="text-xl text-brand-primary font-medium">
				{lecture.artist.nickname}
			</p>
		{/if}

		<div class="flex items-center gap-4 text-content-secondary">
			<span class="flex items-center gap-2">
				<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
					<path
						d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
					/>
				</svg>
				{formatDuration(totalDuration)}
			</span>
			<span class="w-1 h-1 rounded-full bg-content-secondary"></span>
			<span>{lecture.lessons.length}개 세션</span>
		</div>

		<p class="text-content-secondary leading-relaxed mt-2">
			{lecture.description || '이 렉처에 대한 설명이 없습니다.'}
		</p>
	</div>
</div>
