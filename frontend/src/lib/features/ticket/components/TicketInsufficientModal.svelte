<script lang="ts" module>
	export function getInsufficientTitle(): string {
		return '티켓이 부족합니다'
	}

	export function getRefillMessage(): string {
		return '티켓은 매주 충전됩니다'
	}

	export function formatDaysUntilRefill(days: number): string {
		return `다음 충전까지 ${days}일 남았습니다`
	}
</script>

<script lang="ts">
	import { Modal, Button } from 'flowbite-svelte'

	interface Props {
		open: boolean
		daysUntilRefill: number
		onClose: () => void
	}

	let { open = $bindable(), daysUntilRefill, onClose }: Props = $props()
</script>

<Modal bind:open size="xs" autoclose={false} class="w-full">
	<div class="flex flex-col items-center space-y-4 p-4">
		<div class="text-5xl text-yellow-500">
			<svg class="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
				<path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
			</svg>
		</div>
		<h3 class="text-xl font-bold text-white">{getInsufficientTitle()}</h3>
		<p class="text-gray-300 text-center">{getRefillMessage()}</p>
		<p class="text-gray-400 text-sm">{formatDaysUntilRefill(daysUntilRefill)}</p>
		<Button
			type="button"
			class="w-full bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-white font-bold py-3 rounded-lg mt-4"
			onclick={onClose}
		>
			확인
		</Button>
	</div>
</Modal>
