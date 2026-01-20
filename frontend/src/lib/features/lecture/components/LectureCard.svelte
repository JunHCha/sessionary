<script lang="ts">
	import type { LectureInList } from '$lib/api/client'
	import { getThumbnailSrc } from '../utils/format'

	let { lecture }: { lecture: LectureInList } = $props()

	function getTagColor(tag: string): string {
		if (tag === '기본기') return '#734E38'
		if (tag === 'Easy') return '#B2400F'
		if (tag === 'Advanced') return '#662509'
		if (tag === 'Intermediate') return '#FF5C16'
		if (tag === '해석버전') return '#734E38'
		return '#734E38'
	}

	function getTagLabel(tags: unknown[] | null): string[] {
		if (!tags || !Array.isArray(tags) || tags.length === 0) {
			return []
		}
		return tags.map((tag) => String(tag))
	}
</script>

<a
	href="/lecture/{lecture.id}"
	class="group relative w-full max-w-[296px] aspect-[420/339] bg-black rounded-[6px] overflow-hidden block"
>
	<div class="relative w-full h-[70.38%] bg-gray-800">
		<img
			src={getThumbnailSrc(lecture.thumbnail)}
			alt={lecture.title}
			class="w-full h-full object-cover"
		/>
		<div
			class="absolute top-[6.78%] right-[5.95%] w-[27px] h-[30px]"
		>
			<svg
				class="w-full h-full text-white"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
				/>
			</svg>
		</div>
	</div>
	<div class="absolute bottom-[5.31%] left-0 right-[20px] p-0">
		<h5
			class="text-[18px] font-pretendard font-bold leading-[27px] tracking-[-0.02em] text-[#F5F5F5] line-clamp-2 mb-[6px]"
		>
			{lecture.title}
		</h5>
		<p
			class="text-[11px] font-pretendard font-bold leading-[normal] tracking-[-0.01em] text-[#DDDDDD] mb-[10px]"
		>
			{lecture.artist?.nickname || '익명의 아티스트'}
		</p>
		<div class="flex flex-wrap gap-[6px]">
			{#each getTagLabel(lecture.tags) as tag}
				<span
					class="h-[26px] px-[8px] py-[4px] rounded-[6px] flex items-center justify-center text-[11px] font-pretendard font-semibold leading-[18px] tracking-[-0.01em] text-white whitespace-nowrap"
					style="background-color: {getTagColor(tag)}"
				>
					{tag}
				</span>
			{/each}
		</div>
	</div>
</a>
