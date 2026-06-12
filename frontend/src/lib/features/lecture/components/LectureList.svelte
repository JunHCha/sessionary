<script lang="ts">
	import LectureCard from './LectureCard.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { title, lectures }: { title: string; lectures: LectureInList[] } = $props()
</script>

<section
	class="min-h-screen snap-start flex flex-col justify-center xl:items-center bg-black"
>
<div class="w-full max-w-[1200px] px-[20px] py-[8vh] xl:px-0">
	<div
		class="inline-flex items-center gap-[8px] mb-[32px]"
	>
		<h2
			class="text-[24px] leading-[36px] xl:text-[36px] xl:leading-[62px] font-pretendard font-extrabold tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
		>
			{title}
		</h2>
		<div
			class="w-[10px] h-[10px] rounded-full bg-[#FF5C16]"
		></div>
	</div>
	<div
		class="grid grid-cols-2 gap-[12px] md:grid-cols-3 xl:grid-cols-4 xl:gap-[24px]"
	>
		{#each lectures as lecture}
			<LectureCard {lecture} />
		{/each}
	</div>
</div>
</section>
