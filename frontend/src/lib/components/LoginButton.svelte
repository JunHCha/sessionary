<script lang="ts">
	import { goto } from '$app/navigation'
	import { isAuthenticated } from '$lib/stores/auth'
	import LoginForm from './LoginForm.svelte'

	let showLoginModal = false

	function toggleLoginModal() {
		showLoginModal = !showLoginModal
	}

	function handleLogout() {
		localStorage.removeItem('satk')
		localStorage.removeItem('me')
		isAuthenticated.set(false)
		goto('/home')
	}
</script>

{#if $isAuthenticated}
	<button on:click="{handleLogout}">로그아웃</button>
{:else}
	<button on:click="{toggleLoginModal}"> 로그인/회원가입 </button>
{/if}

{#if showLoginModal}
	<div class="modal">
		<LoginForm on:close="{toggleLoginModal}" />
	</div>
{/if}

<style>
	button {
		background-color: #4caf50;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		cursor: pointer;
	}

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
</style>
