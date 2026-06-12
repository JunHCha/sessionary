<script lang="ts">
	import LectureCard from './LectureCard.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { title, lectures }: { title: string; lectures: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col justify-center min-[1280px]:items-center bg-black"
>
<div class="w-full max-w-[1200px] px-[20px] min-[1280px]:px-0">
	<div
		class="inline-flex items-center gap-[8px] mb-[32px]"
	>
		<h2
			class="text-[24px] leading-[36px] min-[1280px]:text-[36px] min-[1280px]:leading-[62px] font-pretendard font-extrabold tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
		>
			{title}
		</h2>
		<div
			class="w-[10px] h-[10px] rounded-full bg-[#FF5C16]"
		></div>
	</div>
	<div
		class="grid grid-cols-2 gap-[12px] md:grid-cols-3 min-[1280px]:grid-cols-4 min-[1280px]:gap-[24px] overflow-y-auto"
	>
		{#each lectures as lecture}
			<LectureCard {lecture} />
		{/each}
	</div>
</div>
</section>
