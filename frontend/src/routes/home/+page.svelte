<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/client'
	import { Heading } from 'flowbite-svelte'
	import LectureListSection from './LectureListSection.svelte'
	import type { LectureList } from '$lib/client'
	import HomeMainSection from './HomeMainSection.svelte'
	import RecommendationSection from './RecommendationSection.svelte'

	let newLectures: LectureList[] = []
	let recommendedLectures: LectureList[] = []

	onMount(async () => {
		try {
			recommendedLectures = (await getLecturesLectureGet({})).data
			newLectures = (await getLecturesLectureGet({})).data
		} catch (error) {
			console.error('Failed to fetch lectures:', error)
		}
	})
</script>

<main class="px-0 mx-0 flex flex-col">
	<HomeMainSection />
	<RecommendationSection {recommendedLectures} />
	<LectureListSection title="새로운 렉쳐" lectures="{newLectures}" />
</main>
