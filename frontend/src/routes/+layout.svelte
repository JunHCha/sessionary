<script context="module">
	import { isAuthenticated } from '$lib/stores/auth';
</script>

<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { OpenAPI } from '$lib/client';
	import { PUBLIC_API_BASE_URL } from '$env/static/public';

	OpenAPI.BASE = PUBLIC_API_BASE_URL;
	OpenAPI.interceptors.request.use((request) => {
		let token = localStorage.getItem('satk');
		if (token) {
			request.headers = request.headers ?? {};
			request.headers['Authorization'] = `Bearer ${token}`;
		}

		return request;
	});

	function checkAuthentication() {
		const token = localStorage.getItem('satk');
		const user = localStorage.getItem('me');
		if (token && user) isAuthenticated.set(true);
		else isAuthenticated.set(false);
	}

	function handleLogout() {
		localStorage.removeItem('satk');
		localStorage.removeItem('me');
		isAuthenticated.set(false); // 로그아웃 상태로 설정
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
		{#if $isAuthenticated}
			<!-- $ 표시를 통해 store를 읽어옴 -->
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
