<script lang="ts">
	import '../app.pcss'
	import { onMount } from 'svelte'
	import { page } from '$app/stores'
	import { initializeApi, usersCurrentUserUserMeGet } from '$lib/api'
	import { setIsAuthenticated } from '$lib/features/auth'
	import { NavBar, Footer } from '$lib/components/layout'
	import type { Snippet } from 'svelte'

	let { data, children }: { data: { env: { PUBLIC_API_BASE_URL: string } }; children: Snippet } =
		$props()

	onMount(() => {
		initializeApi(data.env.PUBLIC_API_BASE_URL)
		checkAuthentication()
	})

	async function checkAuthentication() {
		try {
			const userResponse = await usersCurrentUserUserMeGet()
			if (userResponse) {
				localStorage.setItem('me', JSON.stringify(userResponse))
				setIsAuthenticated(true)
			}
		} catch {
			localStorage.removeItem('me')
			setIsAuthenticated(false)
		}
	}
</script>

<NavBar />

<main>
	<div class="flex-1">
		{@render children()}
	</div>
	<Footer />
</main>

<style>
	:global(body) {
		font-family:
			-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
			'Noto Color Emoji';
		background-color: #0c0c0c;
		color: #ffffff;
	}

	main {
		position: relative;
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main > div:first-child {
		flex: 1 0 auto;
	}
</style>
