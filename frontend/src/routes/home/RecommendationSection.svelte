<script lang="ts">
	import RecommendCard from './RecommendCard.svelte'
	import type { LectureList } from '$lib/client'

	export let recommendedLectures: LectureList[]
</script>

<section class="flex flex-col items-center h-[90vh]">
	<img
		src="images/se-2-png.png"
		srcset="images/se-2-png@2x.png 2x,
	 images/se-2-png@3x.png 3x"
		class="absolute w-full object-contain -z-10"
		alt="se2-png"
	/>
	<span class="flex items-center gap-2 text-5xl font-pretendard font-bold mt-[20rem]">
		🔥 요즘 많이 보는 렉처
		<span class="text-[#FF5C16]">TOP 10</span>
	</span>
	<div class="relative">
		<RecommendCard lectures="{recommendedLectures}" />
	</div>
</section>
