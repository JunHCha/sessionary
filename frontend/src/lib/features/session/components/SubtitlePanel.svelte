<script lang="ts">
	import type { Subtitle } from '$lib/api/client/types.gen'
	import { findActiveSubtitleIndex, formatSubtitleTimestamp } from '../utils'

	let {
		subtitles,
		currentTime = 0,
		onseekrequest
	}: {
		subtitles: Array<Subtitle>
		currentTime?: number
		onseekrequest?: (timeSec: number) => void
	} = $props()

	let scrollContainer: HTMLDivElement
	let activeIndex = $derived(findActiveSubtitleIndex(subtitles, currentTime * 1000))
	let previousActiveIndex = -1

	$effect(() => {
		if (activeIndex === previousActiveIndex) return
		previousActiveIndex = activeIndex
		if (activeIndex >= 0 && scrollContainer) {
			const activeElement = scrollContainer.querySelector('[data-active]')
			activeElement?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
		}
	})

	function handleSubtitleClick(timestampMs: number) {
		onseekrequest?.(timestampMs / 1000)
	}
</script>

<div
	data-testid="subtitle-panel"
	class="flex flex-col bg-[#1a1a1a] rounded-lg border border-[#2a2a2a] h-full overflow-hidden"
>
	{#if subtitles.length === 0}
		<div
			data-testid="subtitle-panel-empty"
			class="flex items-center justify-center h-full"
		>
			<div class="text-center">
				<div class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center">
					<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
						<path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6v-2zm0 4h8v2H6v-2zm10 0h2v2h-2v-2zm-6-4h8v2h-8v-2z" />
					</svg>
				</div>
				<p class="text-[#666] text-sm">자막이 없습니다</p>
			</div>
		</div>
	{:else}
		<div class="px-4 py-3 border-b border-[#2a2a2a]">
			<h3 class="text-sm font-medium text-[#848484]">자막</h3>
		</div>
		<div
			bind:this={scrollContainer}
			class="flex-1 overflow-y-auto px-2 py-2"
		>
			{#each subtitles as subtitle, index}
				<button
					type="button"
					data-testid="subtitle-item-{index}"
					data-active={index === activeIndex ? '' : undefined}
					onclick={() => handleSubtitleClick(subtitle.timestamp_ms)}
					class="w-full text-left px-3 py-2.5 rounded-md transition-colors cursor-pointer
						{index === activeIndex
							? 'bg-[#2a2a2a] text-white'
							: 'text-[#848484] hover:bg-[#222] hover:text-[#ccc]'}"
				>
					<span class="text-xs {index === activeIndex ? 'text-[#FF5C16]' : 'text-[#656565]'} mr-2">
						{formatSubtitleTimestamp(subtitle.timestamp_ms)}
					</span>
					<span class="text-sm">{subtitle.text}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>
