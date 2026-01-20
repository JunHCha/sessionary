<script lang="ts">
	import RecommendCarousel from './RecommendCarousel.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { recommendedLectures = [] }: { recommendedLectures?: LectureInList[] } = $props()
</script>

<section
	class="h-screen snap-start snap-always flex flex-col items-center py-[15vh]"
>
<div class="w-[1280px]">
	<h2
		class="mb-[clamp(2rem,4vh,4rem)] flex items-center text-[clamp(1.8rem,2.8vw,2.3rem)] font-pretendard font-extrabold leading-[clamp(2.5rem,4vw,3.9rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
	>
		<span>요즘 많이 보는 렉처</span>
		<span class="text-[#FF5C16] ml-[clamp(0.5rem,0.75vw,0.75rem)]">TOP 5</span>
	</h2>
	<div class="flex-1 flex items-center justify-center">
		<RecommendCarousel lectures={recommendedLectures} />
	</div>
</div>
</section>
