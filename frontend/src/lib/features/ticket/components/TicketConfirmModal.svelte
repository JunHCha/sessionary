<script lang="ts" module>
	export function getConfirmMessage(): string {
		return '티켓 1개를 사용하여 이 강의에 접근합니다'
	}

	export function getAccessPeriodMessage(): string {
		return '1주간 무제한 시청 가능'
	}

	export function formatTicketCount(count: number): string {
		return `현재 보유 티켓 수: ${count}개`
	}
</script>

<script lang="ts">
	import { Modal, Button } from 'flowbite-svelte'

	interface Props {
		open: boolean
		lectureTitle: string
		lectureThumbnail: string
		ticketCount: number
		onConfirm: () => void
		onCancel: () => void
	}

	let { open = $bindable(), lectureTitle, lectureThumbnail, ticketCount, onConfirm, onCancel }: Props = $props()
</script>

<Modal bind:open size="sm" autoclose={false} class="w-full">
	<div class="flex flex-col items-center space-y-4 p-4">
		<img src={lectureThumbnail} alt={lectureTitle} class="w-full rounded-lg object-cover" />
		<h3 class="text-lg font-bold text-white text-center">{lectureTitle}</h3>
		<p class="text-gray-300 text-center">{getConfirmMessage()}</p>
		<p class="text-gray-400 text-sm">{formatTicketCount(ticketCount)}</p>
		<p class="text-gray-400 text-sm">{getAccessPeriodMessage()}</p>
		<div class="flex gap-3 w-full mt-4">
			<Button
				type="button"
				outline
				class="flex-1 border-gray-600 text-gray-300 hover:bg-gray-700"
				onclick={onCancel}
			>
				취소
			</Button>
			<Button
				type="button"
				class="flex-1 bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-white font-bold"
				onclick={onConfirm}
			>
				확인
			</Button>
		</div>
	</div>
</Modal>
