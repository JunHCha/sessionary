<script lang="ts">
	let { title = 'Subtitle Panel' }: { title?: string } = $props()
</script>

<div
	data-testid="subtitle-panel-placeholder"
	class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] h-[450px]"
>
	<div class="text-center">
		<div class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center">
			<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
				<path
					d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6v-2zm0 4h8v2H6v-2zm10 0h2v2h-2v-2zm-6-4h8v2h-8v-2z"
				/>
			</svg>
		</div>
		<p class="text-[#666] text-sm">{title}</p>
	</div>
</div>
