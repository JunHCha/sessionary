<script lang="ts">
	import LectureCard from './LectureCard.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { title, lectures }: { title: string; lectures: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col justify-center items-center"
>
<div class="w-[1280px]">
	<div
		class="inline-flex items-center gap-[clamp(0.3rem,0.5vw,0.5rem)] mb-[clamp(1.5rem,2vh,2rem)]"
	>
		<h2
			class="text-[clamp(1.5rem,2.6vw,2.25rem)] font-pretendard font-extrabold leading-[clamp(2.2rem,3.9vw,3.9rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
		>
			{title}
		</h2>
		<div
			class="w-[clamp(0.4rem,0.6vw,0.6rem)] h-[clamp(0.4rem,0.6vw,0.6rem)] rounded-full bg-[#FF5C16]"
		></div>
	</div>
	<div
		class="grid grid-cols-4 gap-[24px] overflow-y-auto"
	>
		{#each lectures as lecture}
			<LectureCard {lecture} />
		{/each}
	</div>
</div>
</section>
