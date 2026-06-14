<script lang="ts">
	import { parseSubtitles, type SubtitleRow } from '$lib/features/admin/utils/subtitle-parser'

	let { rows = $bindable([]) }: { rows?: SubtitleRow[] } = $props()

	async function handleFile(event: Event) {
		const input = event.target as HTMLInputElement
		const file = input.files?.[0]
		if (!file) return
		const text = await file.text()
		rows = parseSubtitles(text)
	}

	function addRow() {
		rows = [...rows, { timestamp_ms: 0, text: '' }]
	}

	function removeRow(index: number) {
		rows = rows.filter((_, i) => i !== index)
	}
</script>

<div class="flex flex-col gap-4 font-pretendard" data-testid="subtitle-editor">
	<div class="flex flex-wrap items-center justify-between gap-3">
		<label
			class="group flex cursor-pointer items-center gap-2.5 rounded-xl border border-dashed border-white/[0.12] bg-[#0d0d0d] px-3.5 py-2.5 transition-colors hover:border-[#FF5C16]/50"
		>
			<svg
				class="h-[18px] w-[18px] text-[#9a9a9a] transition-colors group-hover:text-[#FF5C16]"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.8"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M12 16V4M7 9l5-5 5 5" />
				<path d="M5 20h14" />
			</svg>
			<span class="text-[13px] font-medium text-[#cfcfcf]">자막 파일 (.srt/.vtt)</span>
			<input
				type="file"
				accept=".srt,.vtt"
				data-testid="subtitle-file"
				onchange={handleFile}
				class="sr-only"
			/>
		</label>
		<button
			type="button"
			data-testid="subtitle-add-row"
			onclick={addRow}
			class="inline-flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-[13px] font-semibold text-[#FF5C16] transition-colors hover:bg-[#FF5C16]/10"
		>
			<svg
				class="h-4 w-4"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2.2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d="M12 5v14M5 12h14" />
			</svg>
			행 추가
		</button>
	</div>

	{#if rows.length > 0}
		<div class="overflow-hidden rounded-xl border border-white/[0.07]">
			<div
				class="grid grid-cols-[140px_1fr_auto] gap-3 border-b border-white/[0.06] bg-white/[0.02] px-3 py-2 text-[11px] font-semibold uppercase tracking-wide text-[#656565]"
			>
				<span>시작 (ms)</span>
				<span>텍스트</span>
				<span class="text-right">삭제</span>
			</div>
			<div class="flex flex-col">
				{#each rows as row, i (i)}
					<div
						class="grid grid-cols-[140px_1fr_auto] items-center gap-3 border-b border-white/[0.04] px-3 py-2 last:border-b-0 odd:bg-white/[0.01]"
						data-testid="subtitle-row"
					>
						<input
							type="number"
							bind:value={row.timestamp_ms}
							data-testid={`subtitle-ms-${i}`}
							class="w-full rounded-lg border border-white/[0.08] bg-[#0d0d0d] px-2.5 py-1.5 text-[13px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
						<input
							type="text"
							bind:value={row.text}
							data-testid={`subtitle-text-${i}`}
							class="w-full rounded-lg border border-white/[0.08] bg-[#0d0d0d] px-2.5 py-1.5 text-[13px] text-white outline-none transition-colors focus:border-[#FF5C16]"
						/>
						<button
							type="button"
							data-testid={`subtitle-remove-${i}`}
							onclick={() => removeRow(i)}
							aria-label="행 삭제"
							class="flex h-7 w-7 items-center justify-center rounded-lg text-[#656565] transition-colors hover:bg-red-500/10 hover:text-red-400"
						>
							<svg
								class="h-4 w-4"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.8"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<path d="M6 7h12M9 7V5h6v2M10 11v6M14 11v6M5 7l1 13h12l1-13" />
							</svg>
						</button>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<p
			class="rounded-xl border border-dashed border-white/[0.08] py-8 text-center text-[13px] text-[#656565]"
		>
			자막 파일을 올리거나 '행 추가'로 직접 입력하세요
		</p>
	{/if}
</div>
