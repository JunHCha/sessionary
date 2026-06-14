<script lang="ts">
	import { getCurationCurationGet, waitForApiInit } from '$lib/api'
	import type { LectureInList } from '$lib/api'
	import { LectureList, RecommendSection } from '$lib/features/lecture'
	import { HeroSection } from '$lib/components/layout'

	let newLectures = $state<LectureInList[]>([])
	let recommendedLectures = $state<LectureInList[]>([])

	async function fetchCuration() {
		await waitForApiInit()
		try {
			const response = await getCurationCurationGet()
			recommendedLectures = response.data?.TRENDING ?? []
			newLectures = response.data?.NEW ?? []
		} catch (error) {
			console.error('Failed to fetch curation:', error)
			recommendedLectures = []
			newLectures = []
		}
	}

	$effect(() => {
		fetchCuration()
	})
</script>

<div class="min-h-screen snap-y snap-mandatory bg-black">
	<HeroSection />
	<RecommendSection {recommendedLectures} />
	<LectureList title="새로운 렉쳐" lectures={newLectures} />
</div>
