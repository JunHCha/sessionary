<script lang="ts">
	import { createEventDispatcher } from 'svelte'

	const dispatch = createEventDispatcher<{
		download: void
	}>()

	function handleDownload(event: MouseEvent | KeyboardEvent) {
		event.preventDefault()
		dispatch('download')
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault()
			handleDownload(event)
		}
	}
</script>

<div
	class="flex flex-col gap-4 border border-[#454545] rounded-[6px] pt-[25px] pb-[1px] px-[25px] h-[300px]"
>
	<h2 class="font-helvetica font-bold text-[18px] text-[#f5f5f5] leading-[28px] h-[28px]">
		악보 다운로드
	</h2>

	<div
		role="button"
		tabindex="0"
		class="group relative w-full h-[200px] rounded-[6px] overflow-hidden cursor-pointer"
		onclick={handleDownload}
		onkeydown={handleKeyDown}
	>
		<img
			src="/images/sheet-preview.png"
			alt="악보 미리보기"
			class="w-full h-full object-cover"
		/>
		<div
			class="absolute inset-0 flex items-center justify-center bg-[#0c0c0c] opacity-0 group-hover:opacity-80 transition-opacity"
		>
			<button
				class="flex items-center gap-2 bg-[#ff5c16] h-[48px] px-[24px] rounded-[50px] font-helvetica font-bold text-[16px] text-[#f5f5f5]"
			>
				<svg
					class="w-5 h-5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
					/>
				</svg>
				다운로드
			</button>
		</div>
	</div>
</div>
