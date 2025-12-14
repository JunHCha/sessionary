<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/api'
	import type { LectureInList } from '$lib/api'
	import { LectureList, RecommendSection } from '$lib/features/lecture'
	import { HeroSection } from '$lib/components/layout'

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
	<HeroSection />
	<RecommendSection {recommendedLectures} />
	<LectureList title="새로운 렉쳐" lectures="{newLectures}" />
</main>
