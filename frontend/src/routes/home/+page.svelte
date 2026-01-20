<script lang="ts">
	import { getLecturesLectureGet, waitForApiInit } from '$lib/api'
	import type { LectureInList } from '$lib/api'
	import { LectureList, RecommendSection } from '$lib/features/lecture'
	import { HeroSection } from '$lib/components/layout'

	let newLectures = $state<LectureInList[]>([])
	let recommendedLectures = $state<LectureInList[]>([])

	async function fetchLectures() {
		await waitForApiInit()
		try {
			const response = await getLecturesLectureGet({})
			recommendedLectures = response.data || []
			newLectures = response.data || []
		} catch (error) {
			console.error('Failed to fetch lectures:', error)
			recommendedLectures = []
			newLectures = []
		}
	}

	$effect(() => {
		fetchLectures()
	})
</script>

<div class="min-h-screen snap-y snap-mandatory bg-black">
	<HeroSection />
	<RecommendSection {recommendedLectures} />
	<LectureList title="새로운 렉쳐" lectures={newLectures} />
</div>
