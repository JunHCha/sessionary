<script lang="ts">
	import NewLecture from './+page.svelte'

	export let lecture: NewLecture

	function formatDuration(seconds: number): string {
		const minutes = Math.floor(seconds / 60)
		const remainingSeconds = seconds % 60
		return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
	}
</script>

<div
	class="group bg-black rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-100 w-[25rem] mx-[1rem] mb-[5rem]"
>
	<div class="relative">
		<img
			src="{lecture.thumbnail}"
			alt="{lecture.title}"
			class="w-full h-[180px] object-cover transition-all duration-300 group-hover:brightness-50"
		/>
		<div
			class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300"
		>
			<img src="images/mynaui-play-solid.svg" alt="play" class="w-24 h-24" />
		</div>
	</div>
	<div class="p-4">
		<h5 class="mb-2 text-xl font-bold text-white">
			{lecture.title}
		</h5>
		<p class="mb-3 text-[#848484]">세션맨 팝빙구</p>
		<div class="flex flex-wrap gap-2">
			{#each lecture.tags as tag}
				<span class="px-3 py-1 text-sm bg-[#734e38] text-white rounded-md">
					{tag}
				</span>
			{/each}
		</div>
	</div>
</div>
