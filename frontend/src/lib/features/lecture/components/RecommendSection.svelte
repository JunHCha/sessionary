<script lang="ts">
	import RecommendCarousel from './RecommendCarousel.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { recommendedLectures = [] }: { recommendedLectures?: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col xl:items-center py-[10vh] xl:py-[15vh] bg-black"
>
<div class="w-full max-w-[1200px] px-[20px] xl:px-0">
	<h2
		class="mb-[32px] xl:mb-[64px] flex items-center text-[24px] leading-[36px] xl:text-[37px] xl:leading-[62px] font-pretendard font-extrabold tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
	>
		<span>요즘 많이 보는 렉처</span>
		<span class="text-[#FF5C16] ml-[12px]">TOP 5</span>
	</h2>
	<div class="flex-1 flex items-center justify-center">
		<RecommendCarousel lectures={recommendedLectures} />
	</div>
</div>
</section>
