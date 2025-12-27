<script lang="ts">
	import { getLecturesLectureGet, initializeApi } from '$lib/api'
	import type { LectureInList } from '$lib/api'
	import { LectureList, RecommendSection } from '$lib/features/lecture'
	import { HeroSection } from '$lib/components/layout'
	import { OpenAPI } from '$lib/api/client'
	import { env } from '$env/dynamic/public'

	let newLectures = $state<LectureInList[]>([])
	let recommendedLectures = $state<LectureInList[]>([])

	async function fetchLectures() {
		if (!OpenAPI.BASE && env.PUBLIC_API_BASE_URL) {
			initializeApi(env.PUBLIC_API_BASE_URL)
		}
		if (!OpenAPI.BASE) {
			return
		}
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

<main class="px-0 mx-0 flex flex-col">
	<HeroSection />
	<RecommendSection {recommendedLectures} />
	<LectureList title="새로운 렉쳐" lectures={newLectures} />
</main>
