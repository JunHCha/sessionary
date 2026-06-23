<script module lang="ts">
	import type { Subtitle } from '$lib/api/client/types.gen'
	import { findActiveSubtitleIndex } from '../utils'

	const GAP = 30
	const BEND = 54
	const VISIBLE = 2

	export type LineStyle = {
		transform: string
		transformOrigin: string
		opacity: number
		isActive: boolean
		/** 정면 라인만 클릭 가능. 겹쳐 있는 비정면(투명) 라인이 클릭을 가로채지 않게 한다. */
		pointerEvents: 'auto' | 'none'
	}

	/**
	 * 활성 인덱스 기준 상대 위치(offset)에 대한 원통 롤러 라인 스타일 계산.
	 * offset===0 정면(변형 없음), offset<0 위쪽, offset>0 아래쪽.
	 */
	export function computeLineStyle(offset: number): LineStyle {
		const distance = Math.abs(offset)
		const opacity = distance === 0 ? 1 : distance === 1 ? 0.3 : distance <= VISIBLE ? 0.08 : 0

		if (offset === 0) {
			return {
				transform: 'translateY(0)',
				transformOrigin: 'center center',
				opacity,
				isActive: true,
				pointerEvents: 'auto'
			}
		}
		if (offset < 0) {
			return {
				transform: `translateY(${offset * GAP}px) rotateX(${distance * BEND}deg)`,
				transformOrigin: 'center bottom',
				opacity,
				isActive: false,
				pointerEvents: 'none'
			}
		}
		return {
			transform: `translateY(${offset * GAP}px) rotateX(${-distance * BEND}deg)`,
			transformOrigin: 'center top',
			opacity,
			isActive: false,
			pointerEvents: 'none'
		}
	}

	/**
	 * 휠 탐색 시 다음 manualIndex 계산. deltaY>0 → 다음 자막, deltaY<0 → 이전 자막.
	 * 범위를 벗어나지 않게 클램프한다.
	 */
	export function computeWheelIndex(base: number, deltaY: number, length: number): number {
		const next = base + (deltaY > 0 ? 1 : -1)
		return Math.max(0, Math.min(length - 1, next))
	}

	/**
	 * manualIndex가 있으면 우선하고, 없으면 재생 시간(ms) 기준 활성 인덱스를 사용한다.
	 */
	export function resolveActiveIndex(
		manualIndex: number | null,
		subtitles: Array<Subtitle>,
		currentTimeMs: number
	): number {
		return manualIndex ?? findActiveSubtitleIndex(subtitles, currentTimeMs)
	}
</script>

<script lang="ts">
	import { onDestroy } from 'svelte'
	import { formatSubtitleTimestamp } from '../utils'

	/** 휠 탐색이 멈춘 뒤 이 시간(ms)이 지나면 수동 인덱스를 해제하고 재생 시간 추적으로 복귀 */
	const WHEEL_RELEASE_MS = 2000

	let {
		subtitles,
		currentTime = 0,
		onseekrequest
	}: {
		subtitles: Array<Subtitle>
		currentTime?: number
		onseekrequest?: (timeSec: number) => void
	} = $props()

	let manualIndex = $state<number | null>(null)
	let expanded = $state(false)
	let listContainer = $state<HTMLDivElement | undefined>(undefined)

	let activeIndex = $derived(resolveActiveIndex(manualIndex, subtitles, currentTime * 1000))

	let wheelLock = false
	let wheelReleaseTimer: ReturnType<typeof setTimeout> | undefined
	let previousActiveIndex = -1

	$effect(() => {
		if (activeIndex === previousActiveIndex) return
		previousActiveIndex = activeIndex
		if (expanded && activeIndex >= 0 && listContainer) {
			const activeElement = listContainer.querySelector('[data-active]')
			activeElement?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
		}
	})

	function handleClick(timestampMs: number) {
		manualIndex = null
		onseekrequest?.(timestampMs / 1000)
	}

	function handleWheel(event: WheelEvent) {
		event.preventDefault()
		if (wheelLock) return
		wheelLock = true
		setTimeout(() => (wheelLock = false), 90)
		const base = activeIndex < 0 ? 0 : activeIndex
		manualIndex = computeWheelIndex(base, event.deltaY, subtitles.length)
		// 휠이 멈춘 뒤 일정 시간이 지나면 수동 인덱스를 해제해 재생 시간 추적으로 복귀시킨다.
		clearTimeout(wheelReleaseTimer)
		wheelReleaseTimer = setTimeout(() => (manualIndex = null), WHEEL_RELEASE_MS)
	}

	function toggleExpanded() {
		expanded = !expanded
		// 펼치면 전체 탐색 모드 → 휠 탐색 상태를 해제해 재생 위치에 다시 동기화한다.
		if (expanded) {
			clearTimeout(wheelReleaseTimer)
			manualIndex = null
		}
	}

	onDestroy(() => clearTimeout(wheelReleaseTimer))
</script>

<div
	data-testid="subtitle-roller"
	class="subs-card flex flex-col bg-[#1a1a1a] rounded-xl border border-[#2a2a2a] overflow-hidden"
	class:expanded
>
	{#if subtitles.length === 0}
		<div data-testid="subtitle-roller-empty" class="flex items-center justify-center py-10">
			<div class="text-center">
				<div
					class="w-12 h-12 mx-auto mb-3 rounded-full bg-[#2a2a2a] flex items-center justify-center"
				>
					<svg class="w-6 h-6 text-[#666]" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6v-2zm0 4h8v2H6v-2zm10 0h2v2h-2v-2zm-6-4h8v2h-8v-2z"
						/>
					</svg>
				</div>
				<p class="text-[#666] text-sm">자막이 없습니다</p>
			</div>
		</div>
	{:else}
		<div class="flex items-center justify-between px-4 pt-2 pb-0.5">
			<h3 class="text-[11px] font-medium text-[#848484] tracking-wide">자막</h3>
			<button
				type="button"
				data-testid="subtitle-roller-toggle"
				onclick={toggleExpanded}
				class="toggle-btn inline-flex items-center gap-1 text-[11px] text-[#888] px-2 py-[3px] rounded-md hover:bg-[#262626] hover:text-[#ddd] transition-colors"
			>
				<span>{expanded ? '접기' : '펼치기'}</span>
				<svg
					class="chevron w-3.5 h-3.5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path stroke-width="2" stroke-linecap="round" d="M6 9l6 6 6-6" />
				</svg>
			</button>
		</div>

		<div class="roller" onwheel={handleWheel}>
			<div class="roller-stage">
				<div class="roller-track">
					{#each subtitles as subtitle, index (index)}
						{@const style = computeLineStyle(index - activeIndex)}
						<button
							type="button"
							data-testid="subtitle-roller-item-{index}"
							data-active={index === activeIndex ? '' : undefined}
							class="roller-line"
							class:is-active={style.isActive}
							style:transform={style.transform}
							style:transform-origin={style.transformOrigin}
							style:opacity={style.opacity}
							style:pointer-events={style.pointerEvents}
							tabindex={style.isActive ? 0 : -1}
							aria-hidden={style.isActive ? undefined : true}
							onclick={() => handleClick(subtitle.timestamp_ms)}
						>
							<span class="ts">{formatSubtitleTimestamp(subtitle.timestamp_ms)}</span>
							<span class="tx">{subtitle.text}</span>
						</button>
					{/each}
				</div>
			</div>
		</div>

		<div bind:this={listContainer} class="list">
			{#each subtitles as subtitle, index (index)}
				<button
					type="button"
					data-active={index === activeIndex ? '' : undefined}
					class="list-item"
					class:is-active={index === activeIndex}
					onclick={() => handleClick(subtitle.timestamp_ms)}
				>
					<span class="ts">{formatSubtitleTimestamp(subtitle.timestamp_ms)}</span>
					<span class="tx">{subtitle.text}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	.roller {
		position: relative;
		height: 84px;
		perspective: 340px;
		overflow: hidden;
		transition:
			height 0.5s cubic-bezier(0.4, 0, 0.2, 1),
			opacity 0.35s ease;
		-webkit-mask-image: linear-gradient(
			to bottom,
			transparent 0,
			#000 34%,
			#000 66%,
			transparent 100%
		);
		mask-image: linear-gradient(to bottom, transparent 0, #000 34%, #000 66%, transparent 100%);
		cursor: ns-resize;
	}
	.roller-stage {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		transform-style: preserve-3d;
	}
	.roller-track {
		position: relative;
		width: 100%;
		height: 0;
		transform-style: preserve-3d;
	}
	.roller-line {
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		display: flex;
		align-items: center;
		gap: 14px;
		height: 36px;
		margin-top: -18px;
		padding: 0 22px;
		white-space: nowrap;
		text-align: left;
		backface-visibility: hidden;
		transition:
			transform 0.52s cubic-bezier(0.34, 1.05, 0.4, 1),
			opacity 0.45s ease;
		cursor: pointer;
		background: none;
		border: 0;
	}
	.roller-line .ts {
		flex: none;
		font-size: 12px;
		color: #ff5c16;
		font-variant-numeric: tabular-nums;
	}
	.roller-line .tx {
		font-size: 15px;
		color: #9a9a9a;
		overflow: hidden;
		text-overflow: ellipsis;
		transition:
			color 0.3s,
			font-weight 0.3s;
	}
	.roller-line.is-active .tx {
		color: #fff;
		font-weight: 600;
	}
	.roller::before,
	.roller::after {
		content: '';
		position: absolute;
		left: 18px;
		right: 18px;
		height: 1px;
		background: linear-gradient(90deg, transparent, #ff5c1655, transparent);
		z-index: 4;
		pointer-events: none;
	}
	.roller::before {
		top: calc(50% - 18px);
	}
	.roller::after {
		top: calc(50% + 18px);
	}

	.list {
		max-height: 0;
		opacity: 0;
		overflow-y: auto;
		padding: 0 8px;
		transition:
			max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1),
			opacity 0.35s ease 0.1s;
	}
	.expanded .roller {
		height: 0;
		opacity: 0;
		pointer-events: none;
	}
	.expanded .list {
		max-height: 340px;
		opacity: 1;
		padding: 8px;
	}
	.list-item {
		width: 100%;
		text-align: left;
		display: block;
		padding: 10px 12px;
		border-radius: 8px;
		transition: background 0.2s;
		cursor: pointer;
		background: none;
		border: 0;
	}
	.list-item:hover {
		background: #222;
	}
	.list-item.is-active {
		background: #2a2a2a;
	}
	.list-item .ts {
		font-size: 12px;
		color: #656565;
		margin-right: 8px;
		font-variant-numeric: tabular-nums;
	}
	.list-item.is-active .ts {
		color: #ff5c16;
	}
	.list-item .tx {
		font-size: 14px;
		color: #848484;
	}
	.list-item.is-active .tx {
		color: #fff;
	}

	.toggle-btn .chevron {
		transition: transform 0.4s;
	}
	.expanded .toggle-btn .chevron {
		transform: rotate(180deg);
	}
</style>
