<script lang="ts">
	import type { LessonInLecture } from '$lib/api'
	import { formatDuration } from '../utils/format'

	type SessionType = 'play' | 'talk' | 'jam' | 'basic' | 'sheet'

	let { 
		session, 
		index, 
		isCurrent = false 
	}: { 
		session: LessonInLecture
		index: number
		isCurrent?: boolean 
	} = $props()

	const sessionTypes: SessionType[] = ['play', 'talk', 'jam', 'basic', 'sheet']
	let sessionType = $derived(sessionTypes[index % 5] as SessionType)

	const typeConfig: Record<SessionType, { label: string; color: string; bg: string }> = {
		play: { label: 'PLAY', color: '#22C55E', bg: 'rgba(34, 197, 94, 0.15)' },
		talk: { label: 'TALK', color: '#3B82F6', bg: 'rgba(59, 130, 246, 0.15)' },
		jam: { label: 'JAM', color: '#F59E0B', bg: 'rgba(245, 158, 11, 0.15)' },
		basic: { label: 'BASIC', color: '#8B5CF6', bg: 'rgba(139, 92, 246, 0.15)' },
		sheet: { label: 'SHEET', color: '#EC4899', bg: 'rgba(236, 72, 153, 0.15)' }
	}

	let config = $derived(typeConfig[sessionType])
</script>

<button
	class="w-full flex items-center gap-4 p-4 rounded-xl transition-all duration-200 text-left group {!isCurrent ? 'bg-surface-card hover:bg-white/5' : ''}"
	style={isCurrent ? `background: linear-gradient(135deg, ${config.bg}, rgba(255,92,22,0.1))` : ''}
>
	<div
		class="flex-shrink-0 px-3 py-1.5 rounded-lg text-xs font-bold tracking-wider"
		style="background-color: {config.bg}; color: {config.color};"
	>
		{config.label}
	</div>

	<div class="flex-1 min-w-0">
		<p 
			class="font-medium truncate transition-colors"
			class:text-white={isCurrent}
			class:text-content-secondary={!isCurrent}
			class:group-hover:text-white={!isCurrent}
		>
			{session.title}
		</p>
	</div>

	<div class="flex items-center gap-3 flex-shrink-0">
		<span class="text-sm text-content-muted">
			{formatDuration(session.length_sec)}
		</span>
		
		{#if isCurrent}
			<div class="flex items-center gap-1">
				<span class="w-1.5 h-4 bg-brand-primary rounded-full animate-pulse"></span>
				<span class="w-1.5 h-6 bg-brand-primary rounded-full animate-pulse" style="animation-delay: 0.1s"></span>
				<span class="w-1.5 h-3 bg-brand-primary rounded-full animate-pulse" style="animation-delay: 0.2s"></span>
			</div>
		{:else}
			<svg 
				class="w-5 h-5 text-content-muted opacity-0 group-hover:opacity-100 transition-opacity" 
				fill="currentColor" 
				viewBox="0 0 20 20"
			>
				<path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
			</svg>
		{/if}
	</div>
</button>

