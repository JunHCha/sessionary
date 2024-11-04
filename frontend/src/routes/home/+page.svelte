<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/client'
	import { Heading } from 'flowbite-svelte'
	import LectureList from './LectureListSection.svelte'
	import type { LectureList as LectureInList } from '$lib/client'

	let recommendedLectures: LectureInList[] = []
	let newLectures: LectureInList[] = []

	onMount(async () => {
		try {
			// TODO: 추천 강의와 새로운 강의를 가져오는 API 구분하여 호출
			recommendedLectures = (await getLecturesLectureGet({})).data
			newLectures = (await getLecturesLectureGet({})).data
		} catch (error) {
			console.error('Failed to fetch lectures:', error)
		}
	})
</script>

<main>
	<section class="mb-8">
		<Heading tag="h2" customSize="text-2xl font-extrabold" class="mb-4"
			>마지막으로 본 세션</Heading
		>
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
	}
</style>
