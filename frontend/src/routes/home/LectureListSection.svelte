<script lang="ts">
	import NewLecture from './+page.svelte'
	import { Heading } from 'flowbite-svelte'
	import LectureCard from './LectureCard.svelte'

	export let title: string
	export let lectures: NewLecture[]
</script>

<section class="my-[8rem] mx-auto">
	<div class="inline-flex items-center gap-2">
		<Heading tag="h2" customSize="text-4xl font-bold" class="mb-[2rem] text-white"
			>{title}</Heading
		>
		<div class="w-2 h-2 rounded-full bg-[#FF5C16] mb-[2rem] -mt-4"></div>
	</div>
	<div class="grid grid-cols-5 gap-4">
		{#each lectures as lecture}
			<LectureCard {lecture} />
		{/each}
	</div>
</section>

<style>
	/* 스크롤바 숨기기 */
	.hide-scrollbar {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}
	.hide-scrollbar::-webkit-scrollbar {
		display: none; /* Chrome, Safari, Opera */
	}
</style>
