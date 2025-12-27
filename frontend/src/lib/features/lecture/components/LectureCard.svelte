<script lang="ts">
	import type { LectureInList } from '$lib/api/client'

	let { lecture }: { lecture: LectureInList } = $props()
</script>

<a
	href="/lecture/{lecture.id}"
	class="group bg-black rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-100 w-[25rem] mx-[1rem] mb-[5rem] block"
>
	<div class="relative">
		<div
			class="w-full h-[180px] bg-gray-800 flex items-center justify-center transition-all duration-300 group-hover:brightness-50"
		>
			<span class="text-white text-lg">{lecture.thumbnail}</span>
		</div>
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
		<p class="mb-3 text-content-secondary">{lecture.artist}</p>
		<div class="flex flex-wrap gap-2">
			<span class="px-3 py-1 text-sm bg-brand-tag text-white rounded-md">
				{lecture.tags}
			</span>
		</div>
	</div>
</a>
