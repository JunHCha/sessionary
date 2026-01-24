<script lang="ts">
	let { title = 'Playing Guide' }: { title?: string } = $props()
</script>

<div
	data-testid="playing-guide-placeholder"
	class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] w-full overflow-y-auto"
	style="min-height: 150px;"
>
	<div class="text-center">
		<div class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center">
			<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
				<path
					d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
				/>
			</svg>
		</div>
		<p class="text-[#666] text-sm">{title}</p>
	</div>
</div>
