<script lang="ts">
	let { title = 'Tab Sheet' }: { title?: string } = $props()
</script>

<div
	data-testid="tab-sheet-placeholder"
	class="flex items-center justify-center bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] w-full"
	style="min-height: 200px;"
>
	<div class="text-center">
		<div class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center">
			<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
				<path
					d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"
				/>
			</svg>
		</div>
		<p class="text-[#666] text-sm">{title}</p>
	</div>
</div>
