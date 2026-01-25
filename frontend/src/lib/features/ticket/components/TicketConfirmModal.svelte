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
	import { Modal } from '$lib/components'

	interface Props {
		open: boolean
		lectureTitle: string
		lectureThumbnail?: string | null
		ticketCount: number
		onConfirm: () => void
		onCancel: () => void
	}

	let { open = $bindable(), lectureTitle, lectureThumbnail, ticketCount, onConfirm, onCancel }: Props = $props()
</script>

<Modal bind:open size="xs" autoclose={false} class="modal-dark" ariaLabel="티켓 사용 확인">
	<article class="flex flex-col p-6 gap-6">
		<header class="flex flex-col gap-3">
			{#if lectureThumbnail}
				<img
					src={lectureThumbnail}
					alt="{lectureTitle} 썸네일"
					class="w-full h-32 object-cover rounded-md"
				/>
			{/if}
			<h3 class="text-lg font-bold text-[#e5e5e5] text-center">{lectureTitle}</h3>
			<p class="text-sm text-[#b0b0b0] text-center">{getConfirmMessage()}</p>
		</header>

		<section class="flex flex-col gap-2">
			<p class="text-sm text-[#707070] text-center">{formatTicketCount(ticketCount)}</p>
			<p class="text-sm text-[#707070] text-center">{getAccessPeriodMessage()}</p>
		</section>

		<footer class="flex gap-3">
			<button
				type="button"
				class="flex-1 border border-[#1a1a1a] text-[#b0b0b0] hover:bg-[#1a1a1a] font-bold py-2 px-4 rounded-lg transition-colors"
				onclick={onCancel}
			>
				취소
			</button>
			<button
				type="button"
				class="flex-1 bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-[#e5e5e5] font-bold py-2 px-4 rounded-lg transition-colors"
				onclick={onConfirm}
			>
				확인
			</button>
		</footer>
	</article>
</Modal>

