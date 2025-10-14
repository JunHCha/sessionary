<script lang="ts">
	function handleStartClick() {
		// TODO: 시작 버튼 클릭 시 동작 구현
		console.log('시작 버튼 클릭됨')
	}
</script>

<section>
	<div class="relative hero-section h-[100vh]">
		<img src="images/main.png" alt="main" class="w-full h-full" />
		<div class="absolute left-[13%] top-1/2">
			<p class="text-5xl font-pretendard leading-normal font-bold uppercase">
				예배를 예배답게 드리려면,<br />
				결국 노오력이 필요하더라구요.
			</p>
			<p class="my-5 text-xl font-pretendard font-bold text-[#FF5C16] uppercase truncate">
				인도자의 "기타 SOLO~!" 외침이 두렵지 않을 때까지...
			</p>
			<button
				class="bg-[#FF5C16] text-white px-5 py-3 w-[12rem]"
				on:click="{handleStartClick}"
			>
				바로 START
			</button>
		</div>
	</div>
</section>
