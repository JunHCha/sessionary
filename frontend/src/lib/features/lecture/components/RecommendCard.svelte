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

<div class="relative flex-shrink-0 w-full flex flex-col items-center max-w-[900px]">
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
			class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[118px] h-[118px] cursor-pointer hover:scale-110 transition-transform"
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
			class="absolute top-[56px] right-[110px] bg-[#FF5C16] px-[19px] py-[8px] rounded-full flex items-center justify-center"
		>
			<span
				class="text-[18px] font-pretendard font-bold leading-[27px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap"
			>
				TOP {index + 1}
			</span>
		</div>
	</div>
	<div class="mt-[38px] text-center w-full px-[32px]">
		<div
			class="text-[32px] font-pretendard font-bold leading-[46px] tracking-[-0.02em] text-[#F5F5F5] mb-[14px] break-words"
		>
			<span class="text-[#FF5C16]">언제 끝날지 모르는 기도회를 위한 무한반복</span>🔥
		</div>
		<div
			class="text-[21px] font-pretendard font-bold leading-[32px] tracking-[-0.02em] text-[#DDDDDD] break-words"
		>
			{lecture.title || '[위러브Ver] 우리가 주를 더욱 사랑하고 Easy 버전'}
		</div>
	</div>
</div>
