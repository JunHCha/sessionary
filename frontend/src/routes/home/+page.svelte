<script lang="ts">
	import { onMount } from 'svelte'
	import { getLecturesLectureGet } from '$lib/client'
	import { Heading } from 'flowbite-svelte'
	import LectureList from './LectureListSection.svelte'
	import type { LectureList as LectureInList } from '$lib/client'
	import RecommendCard from './RecommendCard.svelte'

	type NewLecture = {
		id: number
		thumbnail: string
		title: string
		artist: string
		description: string
		tags: string[]
		length_sec: number
		lecture_count: number
		time_created: string
		time_updated: string
	}
	let newLectures: NewLecture[] = [
		{
			id: 1,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 2,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 3,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 4,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 5,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 6,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 6,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 7,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 8,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 9,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		},
		{
			id: 10,
			thumbnail: 'thumbnails/gabriel-gurrola-L_36Dxf2FhM-unsplash.png',
			title: "이승윤 '여백 한켠에(Empty Space Above)' Official Video",
			artist: '세션맨 팝빙구',
			description: '',
			tags: ['원곡카피', 'Easy'],
			length_sec: 1,
			lecture_count: 1,
			time_created: '2025-01-01',
			time_updated: '2025-01-01'
		}
	]
	let recommendedLectures: NewLecture[] = newLectures

	onMount(async () => {
		try {
			// TODO: 추천 강의와 새로운 강의를 가져오는 API 구분하여 호출
			// recommendedLectures = (await getLecturesLectureGet({})).data
			// newLectures = (await getLecturesLectureGet({})).data
		} catch (error) {
			console.error('Failed to fetch lectures:', error)
		}
	})
</script>

<main class="px-0 mx-0">
	<div class="relative hero-section h-[100vh]">
		<img src="images/main.png" alt="main" class="w-full h-full" />
		<div class="absolute left-[13%] top-1/2">
			<p class="text-5xl font-pretendard leading-normal font-bold uppercase">
				예배를 예배답게 드리려면,<br />
				결국 노오력이 필요하더라구요.
			</p>
			<p class="my-5 text-xl font-pretendard font-bold text-[#FF5C16] uppercase truncate">
				인도자의 "기타 SOLO~!" 외침이 두렵지 않을 때까지...
			</p>
			<button class="bg-[#FF5C16] text-white px-5 py-3 w-[12rem]">바로 START</button>
		</div>
	</div>
	<section class=" flex flex-col items-center h-[90vh]">
		<!-- 배경 이미지 -->
		<img
			src="images/se-2-png.png"
			srcset="images/se-2-png@2x.png 2x,
		 images/se-2-png@3x.png 3x"
			class="absolute w-full object-contain -z-10"
			alt="se2-png"
		/>
		<!-- <img
			src="images/se-2-png.png"
			srcset="images/se-2-png@2x.png 2x,
		 images/se-2-png@3x.png 3x"
			class="absolute w-[1920px] h-[944px] my-[3px] mb-[156px] px-[552px] pt-[178px] pb-[76px] object-contain -z-10"
			alt="se2-png"
		/> -->
		<span class="flex items-center gap-2 text-5xl font-pretendard font-bold mt-[20rem]">
			🔥 요즘 많이 보는 렉처
			<span class="text-[#FF5C16]">TOP 10</span>
		</span>
		<div class="relative">
			<RecommendCard lectures="{recommendedLectures}" />
		</div>
	</section>

	<LectureList title="새로운 렉쳐" lectures="{newLectures}" />
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
	}
</style>
