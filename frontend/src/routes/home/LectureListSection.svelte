<script lang="ts">
	import { Heading } from 'flowbite-svelte'
	import LectureCard from './LectureCard.svelte'
	import type { LectureInList } from '$lib/client'

	export let title: string
	export let lectures: LectureInList[]
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
