<script lang="ts">
	import { tweened } from 'svelte/motion'
	import { cubicOut } from 'svelte/easing'
	import type { LectureInList } from '$lib/api/client'
	import { getThumbnailSrc } from '../utils/format'

	let { lectures = [] }: { lectures?: LectureInList[] } = $props()

	let currentIndex = $state(0)

	let visibleLectures = $derived.by(() => {
		if (!lectures || !Array.isArray(lectures)) {
			return []
		}
		return lectures.slice(currentIndex, currentIndex + 4)
	})
	let isHovered = $state(false)

	const cardPosition = tweened(0, { duration: 400, easing: cubicOut })

	function nextCard() {
		if (lectures && Array.isArray(lectures) && currentIndex < lectures.length - 1) {
			cardPosition.set(100, { duration: 400 }).then(() => {
				currentIndex++
				cardPosition.set(0, { duration: 0 })
			})
		}
	}
</script>

<p
	class="flex justify-center mt-[2rem] mb-[1rem] text-xl font-pretendard font-bold text-brand-primary uppercase truncate"
>
	쫄지마. 널위해 준비했어. 언제 끝날지 모르는 기도회를 위한 무한반복.
</p>
<span class="flex items-center gap-2 text-4xl font-pretendard font-bold text-center mb-[3rem]">
	{visibleLectures[0]?.title}
</span>
<div class="relative w-full">
	{#each Array.isArray(visibleLectures) && visibleLectures.length > 1 ? visibleLectures.slice(1, 3) : [] as lecture, idx}
		<div
			class="absolute w-[776px] h-[429px] my-12 ml-[22px] rounded-[30px] shadow-[1px_1px_24px_2px_rgba(255,92,22,0.3)] overflow-hidden transition-all duration-400"
			style="
				z-index: -{1 + idx};
				right: -{idx * 20}px;
				top: -{20 + idx * 20}px;
				transform: translateX({$cardPosition}%);
				opacity: {1 - idx * 0.2};
			"
		>
			<div
				class="w-full h-full bg-gray-800 flex items-center justify-center transition-all duration-400"
				style="filter: brightness({100 - idx * 15}%)"
			>
				<img
					src={getThumbnailSrc(lecture.thumbnail)}
					alt={lecture.title}
					class="w-full h-full object-cover transition-all duration-400"
					style="filter: brightness({100 - idx * 15}%)"
				/>
			</div>
		</div>
	{/each}

	<button
		class="relative w-[776px] h-[429px] my-12 ml-[22px] rounded-[30px] shadow-[1px_1px_24px_2px_rgba(255,92,22,0.3)] overflow-hidden cursor-pointer transition-all duration-400"
		onclick={nextCard}
		onmouseenter={() => (isHovered = true)}
		onmouseleave={() => (isHovered = false)}
		onkeydown={(e) => e.key === 'Enter' && nextCard()}
		style="
			transform: {isHovered
			? `perspective(1000px) translateZ(20px) translateX(${$cardPosition}%)`
			: `perspective(1000px) translateX(${$cardPosition}%)`};
			opacity: {1 - $cardPosition / 100};
		"
	>
		<div class="w-full h-full bg-gray-800 flex items-center justify-center">
			<img
				src={getThumbnailSrc(visibleLectures[0]?.thumbnail)}
				alt={visibleLectures[0]?.title}
				class="w-full h-full object-cover"
			/>
		</div>

		{#if isHovered}
			<div
				class="absolute bottom-0 right-0 w-16 h-16 bg-gradient-to-br from-transparent to-white/10
				transform origin-bottom-right transition-transform duration-300"
				style="transform: rotate(-5deg) translate(5px, 5px);"
			></div>
		{/if}
	</button>
</div>
