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

<div class="flex flex-col gap-2">
	<span class="text-sm">{label}</span>
	<div class="flex items-center gap-3 flex-wrap">
		<input
			type="file"
			{accept}
			data-testid={`${testidPrefix}-input`}
			onchange={handleSelect}
			class="text-xs"
		/>
		<Button
			data-testid={`${testidPrefix}-btn`}
			color="alternative"
			size="xs"
			disabled={!selected || status === 'uploading'}
			onclick={upload}
		>
			업로드
		</Button>
		<span class="text-xs" data-testid={`${testidPrefix}-status`}>
			{#if status === 'uploading'}
				업로드 중...
			{:else if status === 'done'}
				완료
			{:else if status === 'error'}
				실패
			{/if}
		</span>
	</div>
</div>
