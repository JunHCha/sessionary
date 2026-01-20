<script lang="ts">
	import RecommendCard from './RecommendCard.svelte'
	import type { LectureInList } from '$lib/api/client'

	let { lectures = [] }: { lectures?: LectureInList[] } = $props()

	let currentIndex = $state(0)

	let topLectures = $derived.by(() => {
		if (!lectures || !Array.isArray(lectures)) {
			return []
		}
		return lectures.slice(0, 5)
	})

	let canGoPrevious = $derived(currentIndex > 0)
	let canGoNext = $derived(currentIndex < topLectures.length - 1)

	function goToPrevious() {
		if (canGoPrevious) {
			currentIndex--
		}
	}

	function goToNext() {
		if (canGoNext) {
			currentIndex++
		}
	}

	function goToSlide(index: number) {
		if (index >= 0 && index < topLectures.length) {
			currentIndex = index
		}
	}
</script>

<div class="relative w-full max-w-[1280px] mx-auto">
	<div class="relative overflow-hidden">
		<div
			class="flex transition-transform duration-500 ease-in-out"
			style="transform: translateX(-{currentIndex * 100}%)"
		>
			{#each topLectures as lecture, index}
				<div class="w-full flex-shrink-0 flex justify-center">
					<RecommendCard {lecture} {index} />
				</div>
			{/each}
		</div>
	</div>

	{#if topLectures.length > 1}
		<div class="carousel-controls absolute inset-0 pointer-events-none">
			<button
				type="button"
				onclick={goToPrevious}
				disabled={!canGoPrevious}
				class="absolute left-[32px] top-1/2 -translate-y-1/2 w-[64px] h-[64px] bg-[#0C0C0C] bg-opacity-60 hover:bg-opacity-80 rounded-full flex items-center justify-center text-white transition-all disabled:opacity-30 disabled:cursor-not-allowed pointer-events-auto"
				aria-label="이전 슬라이드"
			>
				<svg
					class="w-[32px] h-[32px]"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 19l-7-7 7-7"
					/>
				</svg>
			</button>

			<button
				type="button"
				onclick={goToNext}
				disabled={!canGoNext}
				class="absolute right-[32px] top-1/2 -translate-y-1/2 w-[64px] h-[64px] bg-[#0C0C0C] bg-opacity-60 hover:bg-opacity-80 rounded-full flex items-center justify-center text-white transition-all disabled:opacity-30 disabled:cursor-not-allowed pointer-events-auto"
				aria-label="다음 슬라이드"
			>
				<svg
					class="w-[32px] h-[32px]"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5l7 7-7 7"
					/>
				</svg>
			</button>
		</div>

		<div
			class="carousel-indicators flex justify-center gap-[12px] mt-[32px]"
		>
			{#each topLectures as _, index}
				<button
					type="button"
					onclick={() => goToSlide(index)}
					class="h-[12px] rounded-full transition-all {index ===
					currentIndex
						? 'bg-[#FF5C16] w-[32px]'
						: 'bg-[#666666] hover:bg-[#888888] w-[12px]'}"
					aria-label="슬라이드 {index + 1}로 이동"
				></button>
			{/each}
		</div>
	{/if}
</div>
