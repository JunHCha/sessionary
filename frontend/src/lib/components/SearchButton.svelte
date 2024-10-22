<script lang="ts">
	let showSearchModal = false

	function toggleSearchModal() {
		showSearchModal = !showSearchModal
	}

	function handleSearch(event: Event) {
		event.preventDefault()
		// TODO: 검색 로직 구현
		console.log('Search submitted')
		toggleSearchModal()
	}
</script>

<button on:click="{toggleSearchModal}">검색</button>

{#if showSearchModal}
	<div class="modal">
		<form on:submit="{handleSearch}">
			<input type="text" placeholder="검색어를 입력하세요" />
			<button type="submit">검색</button>
		</form>
		<button on:click="{toggleSearchModal}">닫기</button>
	</div>
{/if}

<style>
	.modal {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background-color: white;
		padding: 2rem;
		border-radius: 5px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}

	form {
		display: flex;
		gap: 0.5rem;
	}

	input {
		padding: 0.5rem;
	}

	button {
		padding: 0.5rem 1rem;
		cursor: pointer;
	}
</style>
