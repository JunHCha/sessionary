<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/client'
	import LectureList from '$lib/components/LectureListSection.svelte'
	import type { LectureList as LectureInList } from '$lib/client'

	let recommendedLectures: LectureInList[] = []
	let newLectures: LectureInList[] = []

	onMount(async () => {
		try {
			// 추천 강의와 새로운 강의를 가져오는 API 호출
			recommendedLectures = (await getLecturesLectureGet({})).data
			newLectures = (await getLecturesLectureGet({})).data
		} catch (error) {
			console.error('Failed to fetch lectures:', error)
		}
	})
</script>

<main>
	<section class="last-session">
		<h2>마지막으로 본 세션</h2>
		<p class="placeholder">최근에 본 세션이 없습니다. 강의를 시작해보세요!</p>
	</section>

	<LectureList title="추천하는 렉쳐" lectures="{recommendedLectures}" />
	<LectureList title="새롭게 추가된 렉쳐" lectures="{newLectures}" />
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		padding: 2rem;
		background-color: lavender;
	}

	h2 {
		margin-bottom: 1rem;
	}

	.last-session {
		background: #fff;
		border-radius: 8px;
		padding: 1rem;
		margin-bottom: 2rem;
	}

	.placeholder {
		color: #666;
		font-style: italic;
	}
</style>
