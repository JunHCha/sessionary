<script lang="ts">
	import type { LectureDetail } from '$lib/api'

	let { lecture }: { lecture: LectureDetail } = $props()

	function formatDate(iso: string): string {
		const d = new Date(iso)
		if (Number.isNaN(d.getTime())) return '-'
		const y = d.getFullYear()
		const m = String(d.getMonth() + 1).padStart(2, '0')
		const day = String(d.getDate()).padStart(2, '0')
		return `${y}.${m}.${day}`
	}

	let updated = $derived(formatDate(lecture.time_updated))
	let created = $derived(formatDate(lecture.time_created))
</script>

<div class="rounded-[14px] border border-[#242424] bg-[#141414] p-5">
	<h3 class="mb-[14px] text-[15px] font-semibold text-[#f5f5f5]">수강 정보</h3>
	<div class="flex flex-col gap-3">
		<div class="flex justify-between text-[14px]">
			<span class="text-[#656565]">제공 자료</span>
			<span class="font-semibold text-[#c9c9c9]">악보 PDF · 자막</span>
		</div>
		<div class="flex justify-between text-[14px]">
			<span class="text-[#656565]">수강 방식</span>
			<span class="font-semibold text-[#c9c9c9]">티켓 1장</span>
		</div>
		<div class="flex justify-between text-[14px]">
			<span class="text-[#656565]">업데이트</span>
			<span class="font-semibold text-[#c9c9c9]">{updated}</span>
		</div>
		<div class="flex justify-between text-[14px]">
			<span class="text-[#656565]">등록일</span>
			<span class="font-semibold text-[#c9c9c9]">{created}</span>
		</div>
	</div>
</div>
