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

<div class="flex flex-col gap-3" data-testid="subtitle-editor">
	<div class="flex items-center gap-3">
		<label class="text-sm">
			자막 파일 (.srt/.vtt)
			<input
				type="file"
				accept=".srt,.vtt"
				data-testid="subtitle-file"
				onchange={handleFile}
				class="block mt-1 text-xs"
			/>
		</label>
		<button
			type="button"
			data-testid="subtitle-add-row"
			onclick={addRow}
			class="text-sm text-[#FF5C16] hover:underline"
		>
			+ 행 추가
		</button>
	</div>

	<div class="flex flex-col gap-2">
		{#each rows as row, i (i)}
			<div class="flex items-center gap-2" data-testid="subtitle-row">
				<input
					type="number"
					bind:value={row.timestamp_ms}
					data-testid={`subtitle-ms-${i}`}
					class="w-28 bg-black border border-[#333] rounded px-2 py-1 text-sm focus:border-[#FF5C16] outline-none"
				/>
				<input
					type="text"
					bind:value={row.text}
					data-testid={`subtitle-text-${i}`}
					class="flex-1 bg-black border border-[#333] rounded px-2 py-1 text-sm focus:border-[#FF5C16] outline-none"
				/>
				<button
					type="button"
					data-testid={`subtitle-remove-${i}`}
					onclick={() => removeRow(i)}
					class="text-[#888] hover:text-red-400 text-sm"
				>
					삭제
				</button>
			</div>
		{/each}
	</div>
</div>
