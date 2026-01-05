<script lang="ts">
	import type { LectureInList } from '$lib/api/client'
	import { getThumbnailSrc } from '../utils/format'

	let {
		lecture,
		index
	}: {
		lecture: LectureInList
		index: number
	} = $props()
</script>

<div class="relative flex-shrink-0 w-full flex flex-col items-center max-w-[70vw]">
	<div class="relative w-full aspect-[1455/816.556]">
		<img
			src={getThumbnailSrc(lecture.thumbnail)}
			alt={lecture.title}
			class="w-full h-full object-cover object-center"
		/>
		<div class="absolute inset-0 bg-[#0C0C0C] opacity-80"></div>
		<button
			type="button"
			aria-label="강의 재생"
			class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[clamp(4rem,7vw,7.4rem)] h-[clamp(4rem,7vw,7.4rem)] cursor-pointer hover:scale-110 transition-transform"
		>
			<svg
				class="w-full h-full text-white"
				fill="currentColor"
				viewBox="0 0 24 24"
				xmlns="http://www.w3.org/2000/svg"
				aria-hidden="true"
			>
				<path d="M8 5v14l11-7z" fill-rule="evenodd" clip-rule="evenodd" />
			</svg>
		</button>
		<div
			class="absolute top-[clamp(2rem,3vh,3.5rem)] right-[clamp(3rem,7vw,6.9rem)] bg-[#FF5C16] px-[clamp(0.5rem,1.0vw,1.2rem)] py-[clamp(0.2rem,0.4vh,0.5rem)] rounded-full flex items-center justify-center"
		>
			<span
				class="text-[clamp(0.75rem,1.1vw,1.1rem)] font-pretendard font-bold leading-[clamp(1.2rem,1.7vw,1.7rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
			>
				TOP {index + 1}
			</span>
		</div>
	</div>
	<div class="mt-[clamp(1.5rem,2.4vh,2.4rem)] text-center w-full px-[clamp(1rem,2vw,2rem)]">
		<div
			class="text-[clamp(1.3rem,2vw,2rem)] font-pretendard font-bold leading-[clamp(1.8rem,2.9vw,2.9rem)] tracking-[-0.02em] text-[#F5F5F5] mb-[clamp(0.6rem,1vh,0.9rem)] break-words"
		>
			<span class="text-[#FF5C16]">언제 끝날지 모르는 기도회를 위한 무한반복</span>🔥
		</div>
		<div
			class="text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#DDDDDD] break-words"
		>
			{lecture.title || '[위러브Ver] 우리가 주를 더욱 사랑하고 Easy 버전'}
		</div>
	</div>
</div>
