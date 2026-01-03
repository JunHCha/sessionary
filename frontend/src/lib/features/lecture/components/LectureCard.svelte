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
	class="group relative w-full max-w-[clamp(15rem,26vw,26.25rem)] aspect-[420/339] bg-black rounded-[clamp(0.3rem,0.4vw,0.4rem)] overflow-hidden block"
>
	<div class="relative w-full h-[70.38%] bg-gray-800">
		<img
			src={getThumbnailSrc(lecture.thumbnail)}
			alt={lecture.title}
			class="w-full h-full object-cover"
		/>
		<div
			class="absolute top-[6.78%] right-[5.95%] w-[clamp(1rem,1.7vw,1.7rem)] h-[clamp(1.2rem,1.9vw,1.9rem)]"
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
	<div class="absolute bottom-[5.31%] left-0 right-[clamp(0.8rem,1.25vw,1.25rem)] p-0">
		<h5
			class="text-[clamp(0.75rem,1.1vw,1.1rem)] font-pretendard font-bold leading-[clamp(1.2rem,1.7vw,1.7rem)] tracking-[-0.02em] text-[#F5F5F5] line-clamp-2 mb-[clamp(0.3rem,0.4vw,0.4rem)]"
		>
			{lecture.title}
		</h5>
		<p
			class="text-[clamp(0.45rem,0.7vw,0.7rem)] font-pretendard font-bold leading-[normal] tracking-[-0.01em] text-[#DDDDDD] mb-[clamp(0.4rem,0.6vw,0.6rem)]"
		>
			{lecture.artist || ''}
		</p>
		<div class="flex flex-wrap gap-[clamp(0.3rem,0.4vw,0.4rem)]">
			{#each getTagLabel(lecture.tags) as tag}
				<span
					class="h-[clamp(1.2rem,1.6vw,1.6rem)] px-[clamp(0.4rem,0.5vw,0.5rem)] py-[clamp(0.2rem,0.25vw,0.25rem)] rounded-[clamp(0.3rem,0.4vw,0.4rem)] flex items-center justify-center text-[clamp(0.45rem,0.7vw,0.7rem)] font-pretendard font-semibold leading-[clamp(0.9rem,1.1vw,1.1rem)] tracking-[-0.01em] text-white whitespace-nowrap"
					style="background-color: {getTagColor(tag)}"
				>
					{tag}
				</span>
			{/each}
		</div>
	</div>
</a>
