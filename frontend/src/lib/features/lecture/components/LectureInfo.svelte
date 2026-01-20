<script lang="ts">
	import type { LectureDetail } from '$lib/api'
	import { getThumbnailSrc } from '../utils/format'

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
</script>

<div class="flex flex-col">
	<!-- Thumbnail with bookmark -->
	<div class="relative w-[480px] h-[320px] rounded-[6px] overflow-hidden">
		<img
			src={getThumbnailSrc(lecture.thumbnail)}
			alt={lecture.title}
			class="w-full h-full object-cover"
		/>
		<button class="absolute top-6 right-6" aria-label="북마크">
			<svg width="27" height="30" viewBox="0 0 27 30" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M1 4C1 2.34315 2.34315 1 4 1H23C24.6569 1 26 2.34315 26 4V28L13.5 21L1 28V4Z" stroke="white" stroke-width="2"/>
			</svg>
		</button>
	</div>

	<!-- Tags -->
	<div class="flex gap-2 mt-[26px]">
		{#if lecture.tags && lecture.tags.length > 0}
			{#each lecture.tags as tag}
				<span
					class="h-[34px] px-[10px] flex items-center justify-center rounded-[6px] font-bold text-[15px] text-white"
					style="background-color: {getTagColor(String(tag))}; font-family: Helvetica, Arial, sans-serif;"
				>
					{tag}
				</span>
			{/each}
		{/if}
	</div>

	<!-- Title -->
	<h1
		class="max-w-[417px] mt-[26px] font-bold text-[24px] leading-[36px] tracking-[-0.48px] text-[#f5f5f5]"
		style="font-family: Helvetica, Arial, sans-serif;"
	>
		{lecture.title}
	</h1>

	<!-- Artist -->
	{#if lecture.artist}
		<p
			class="mt-2 font-bold text-[15px] text-[#ddd]"
			style="font-family: Helvetica, Arial, sans-serif;"
		>
			{lecture.artist.nickname}
		</p>
	{/if}

	<!-- Description -->
	<p
		class="max-w-[478px] mt-4 text-[16px] leading-[28px] tracking-[-0.32px] text-[#ddd]"
		style="font-family: Helvetica, Arial, sans-serif;"
	>
		{lecture.description || '이 렉처에 대한 설명이 없습니다.'}
	</p>
</div>
