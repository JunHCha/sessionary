<script lang="ts">
	import { Button } from 'flowbite-svelte'

	let {
		label,
		accept,
		testidPrefix,
		onUpload
	}: {
		label: string
		accept: string
		testidPrefix: string
		onUpload: (file: File) => Promise<void>
	} = $props()

	let selected = $state<File | null>(null)
	let status = $state<'idle' | 'uploading' | 'done' | 'error'>('idle')

	function handleSelect(event: Event) {
		const input = event.target as HTMLInputElement
		selected = input.files?.[0] ?? null
		status = 'idle'
	}

	async function upload() {
		if (!selected) return
		status = 'uploading'
		try {
			await onUpload(selected)
			status = 'done'
		} catch (e) {
			status = 'error'
			console.error(e)
		}
	}
</script>

<div class="flex flex-col gap-2.5 font-pretendard">
	<span class="text-[13px] font-semibold text-[#bdbdbd]">{label}</span>

	<label
		class="group flex cursor-pointer items-center gap-3 rounded-xl border border-dashed border-white/[0.12] bg-[#0d0d0d] px-3.5 py-3 transition-colors hover:border-[#FF5C16]/50"
	>
		<span
			class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/[0.05] text-[#9a9a9a] transition-colors group-hover:text-[#FF5C16]"
		>
			<svg
				class="h-[18px] w-[18px]"
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
		</span>
		<span class="flex min-w-0 flex-col">
			<span class="truncate text-[13px] font-medium text-white">
				{selected ? selected.name : '파일 선택'}
			</span>
			<span class="truncate text-[11px] text-[#656565]">{accept}</span>
		</span>
		<input
			type="file"
			{accept}
			data-testid={`${testidPrefix}-input`}
			onchange={handleSelect}
			class="sr-only"
		/>
	</label>

	<div class="flex items-center gap-2.5">
		<Button
			data-testid={`${testidPrefix}-btn`}
			color="alternative"
			size="xs"
			class="font-pretendard font-semibold"
			disabled={!selected || status === 'uploading'}
			onclick={upload}
		>
			업로드
		</Button>
		<span
			class="inline-flex items-center gap-1.5 text-[12px] font-medium
				{status === 'done' ? 'text-emerald-400' : status === 'error' ? 'text-red-400' : 'text-[#848484]'}"
			data-testid={`${testidPrefix}-status`}
		>
			{#if status === 'uploading'}
				<span
					class="h-3 w-3 animate-spin rounded-full border-2 border-white/20 border-t-[#FF5C16]"
				></span>
				업로드 중...
			{:else if status === 'done'}
				<svg
					class="h-3.5 w-3.5"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2.4"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M20 6 9 17l-5-5" />
				</svg>
				완료
			{:else if status === 'error'}
				실패
			{/if}
		</span>
	</div>
</div>
