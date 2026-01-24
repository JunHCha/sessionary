<script lang="ts">
	let { title = 'Video Player' }: { title?: string } = $props()
</script>

<div
	data-testid="video-player-placeholder"
	class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a]"
	style="min-height: 300px;"
>
	<div class="text-center">
		<div class="w-16 h-16 mx-auto mb-4 rounded-full bg-[#2a2a2a] flex items-center justify-center">
			<svg class="w-8 h-8 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
				<path d="M8 5v14l11-7z" />
			</svg>
		</div>
		<p class="text-[#666] text-sm">{title}</p>
	</div>
</div>
