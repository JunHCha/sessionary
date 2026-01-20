<script lang="ts">
	import LectureCard from './LectureCard.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { title, lectures }: { title: string; lectures: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col justify-center min-[1280px]:items-center min-w-[1280px] bg-black"
>
<div class="w-[1200px] ml-[40px] min-[1280px]:ml-0">
	<div
		class="inline-flex items-center gap-[8px] mb-[32px]"
	>
		<h2
			class="text-[36px] font-pretendard font-extrabold leading-[62px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
		>
			{title}
		</h2>
		<div
			class="w-[10px] h-[10px] rounded-full bg-[#FF5C16]"
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
