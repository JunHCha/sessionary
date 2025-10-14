<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/client'
	import LectureListSection from './LectureListSection.svelte'
	import type { LectureInList } from '$lib/client'
	import HomeMainSection from './HomeMainSection.svelte'
	import RecommendationSection from './RecommendationSection.svelte'

	let newLectures: LectureInList[] = []
	let recommendedLectures: LectureInList[] = []

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
