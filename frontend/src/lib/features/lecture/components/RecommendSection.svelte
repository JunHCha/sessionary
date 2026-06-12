<script lang="ts">
	import RecommendCarousel from './RecommendCarousel.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { recommendedLectures = [] }: { recommendedLectures?: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col min-[1280px]:items-center py-[10vh] min-[1280px]:py-[15vh] bg-black"
>
<div class="w-full max-w-[1200px] px-[20px] min-[1280px]:px-0">
	<h2
		class="mb-[32px] min-[1280px]:mb-[64px] flex items-center text-[24px] leading-[36px] min-[1280px]:text-[37px] min-[1280px]:leading-[62px] font-pretendard font-extrabold tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
	>
		<span>요즘 많이 보는 렉처</span>
		<span class="text-[#FF5C16] ml-[12px]">TOP 5</span>
	</h2>
	<div class="flex-1 flex items-center justify-center">
		<RecommendCarousel lectures={recommendedLectures} />
	</div>
</div>
</section>
