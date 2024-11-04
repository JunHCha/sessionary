<script lang="ts">
	import type { LectureList as LectureInList } from '$lib/client'
	import { Card, ImagePlaceholder } from 'flowbite-svelte'

	export let lecture: LectureInList

	function formatDuration(seconds: number): string {
		const minutes = Math.floor(seconds / 60)
		const remainingSeconds = seconds % 60
		return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
	}
</script>

<Card class="space-y-5 w-64 hover:shadow-lg transition-shadow duration-100">
	<ImagePlaceholder imgHeight="48" imgOnly />
	<h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">
		{lecture.title}
	</h5>
	<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
		{lecture.description}
	</p>
	<p class="mb-1 italic dark:text-gray-200">
		{formatDuration(lecture.length_sec)}
	</p>
</Card>
