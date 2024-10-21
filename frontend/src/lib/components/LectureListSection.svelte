<script lang="ts">
	import type { LectureList } from '$lib/client'
	import LectureCard from './LectureCard.svelte'

	export let title: string
	export let lectures: LectureList[]
</script>

<section>
	<h2>{title}</h2>
	<div class="lecture-list">
		{#each lectures as lecture}
			<LectureCard {lecture} />
		{/each}
	</div>
</section>

<style>
	section {
		margin-bottom: 2rem;
	}

	h2 {
		margin-bottom: 1rem;
	}

	.lecture-list {
		display: flex;
		overflow-x: auto;
		padding-bottom: 1rem;
	}
</style>
