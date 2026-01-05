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

<div class="flex flex-col gap-4">
	<h2 class="text-lg font-pretendard font-bold text-white">악보 미리보기</h2>

	<div
		role="button"
		tabindex="0"
		class="group relative w-auto h-[30vh] flex items-center justify-center rounded-xl overflow-hidden bg-surface-card cursor-pointer"
		onclick={handleDownload}
		onkeydown={handleKeyDown}
	>
		<img
			src="/images/sheet-preview.png"
			alt="악보 미리보기"
			class="mx-auto w-auto h-full object-cover group-hover:opacity-50"
		/>
		<div
			class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100"
		>
			<svg
				class="w-12 h-12 text-white"
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
		</div>
	</div>
</div>
