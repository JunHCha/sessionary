<script lang="ts">
	import type { LectureDetail } from '$lib/api'
	import { formatTotalLength, getDifficultyLabel } from '../utils/curriculum'

	let { lecture }: { lecture: LectureDetail } = $props()

	const TAG_COLORS: Record<string, string> = {
		'기본기': '#734e38',
		'Easy': '#b2400f',
		'Intermediate': '#FF5C16',
		'Advanced': '#662509',
		'해석버전': '#734e38'
	}

	function getTagColor(tag: string): string {
		return TAG_COLORS[tag] || '#734e38'
	}

	let sessionCount = $derived(lecture.lessons?.length ?? 0)
	let totalLength = $derived(formatTotalLength(lecture.length_sec))
	let difficulty = $derived(getDifficultyLabel(lecture.tags))
</script>

<div class="flex min-w-0 flex-col">
	<!-- Tags -->
	{#if lecture.tags && lecture.tags.length > 0}
		<div class="mb-4 flex flex-wrap gap-2">
			{#each lecture.tags as tag}
				<span
					class="flex items-center justify-center rounded-[7px] px-[12px] py-[6px] text-[13px] font-bold text-white"
					style="background-color: {getTagColor(String(tag))}; font-family: Helvetica, Arial, sans-serif;"
				>
					{tag}
				</span>
			{/each}
		</div>
	{/if}

	<!-- Title -->
	<h1
		class="text-[24px] font-bold leading-[1.3] tracking-[-0.5px] text-[#f5f5f5] lg:text-[30px]"
		style="font-family: Helvetica, Arial, sans-serif;"
	>
		{lecture.title}
	</h1>

	<!-- Artist -->
	{#if lecture.artist}
		<p class="mt-4 text-[15px] font-bold text-[#ddd]" style="font-family: Helvetica, Arial, sans-serif;">
			{lecture.artist.nickname}
		</p>
	{/if}

	<!-- Description -->
	<p class="mt-4 text-[15px] leading-[1.75] tracking-[-0.3px] text-[#c9c9c9]">
		{lecture.description || '이 렉처에 대한 설명이 없습니다.'}
	</p>

	<!-- Stats -->
	<div class="mt-6 flex border-t border-[#242424] pt-6">
		<div class="flex flex-1 flex-col gap-1 pr-5">
			<span class="text-[12px] text-[#656565]">세션</span>
			<span class="text-[19px] font-bold text-[#f5f5f5]"
				>{sessionCount}<span class="text-[13px] font-medium text-[#848484]"> 개</span></span
			>
		</div>
		<div class="flex flex-1 flex-col gap-1 border-l border-[#242424] px-5">
			<span class="text-[12px] text-[#656565]">총 길이</span>
			<span class="text-[19px] font-bold text-[#f5f5f5]">{totalLength}</span>
		</div>
		<div class="flex flex-1 flex-col gap-1 border-l border-[#242424] pl-5">
			<span class="text-[12px] text-[#656565]">난이도</span>
			<span class="text-[19px] font-bold text-[#f5f5f5]">{difficulty}</span>
		</div>
	</div>
</div>
