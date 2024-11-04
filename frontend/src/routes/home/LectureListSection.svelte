<script lang="ts">
	import type { LectureList } from '$lib/client'
	import { Heading } from 'flowbite-svelte'
	import LectureCard from './LectureCard.svelte'

	export let title: string
	export let lectures: LectureList[]
</script>

<section class="mb-8">
	<Heading tag="h2" customSize="text-2xl font-extrabold" class="mb-4">{title}</Heading>
	<div class="flex overflow-x-auto gap-4 pb-2 hide-scrollbar">
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
