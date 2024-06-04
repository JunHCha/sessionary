<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let isAuthenticated = false;

	function checkAuthentication() {
		const token = localStorage.getItem('satk');
		const user = localStorage.getItem('me');
		if (token && user) {
			try {
				const parsedUser = JSON.parse(user);
				if (parsedUser && parsedUser.id) {
					isAuthenticated = true;
				} else {
					handleLogout();
				}
			} catch (error) {
				console.error('Token validation error:', error);
				handleLogout();
			}
		} else {
			handleLogout();
		}
	}

	function handleLogout() {
		localStorage.removeItem('satk');
		localStorage.removeItem('me');
		isAuthenticated = false;
		goto('/login');
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			checkAuthentication();
		}
	});
</script>

<main>
	<nav>
		<button on:click={() => goto('/home')}>로고</button>
		<button on:click={() => goto('/menu01')}>메뉴01</button>
		<button on:click={() => goto('/menu02')}>메뉴02</button>
		<button on:click={() => goto('/menu03')}>메뉴03</button>
		{#if isAuthenticated}
			<button on:click={handleLogout}>로그아웃</button>
		{:else}
			<button on:click={() => goto('/login')}>로그인 / 회원가입</button>
		{/if}
	</nav>
	<slot />
</main>

<style>
	nav {
		display: flex;
		gap: 1rem;
		background-color: #f0f0f0;
		padding: 1rem;
	}

	button {
		background-color: #e0e0e0;
		border: none;
		padding: 0.5rem 1rem;
		cursor: pointer;
	}

	main {
		background-color: lavender;
		min-height: 100vh;
	}
</style>
