<script lang="ts">
	import '../app.pcss'
	import { onMount } from 'svelte'
	import { initializeApi, usersCurrentUserUserMeGet } from '$lib/api'
	import { isAuthenticated } from '$lib/features/auth'
	import { NavBar, Footer } from '$lib/components/layout'

	export let data: { env: { PUBLIC_API_BASE_URL: string } }

	initializeApi(data.env.PUBLIC_API_BASE_URL)

	async function checkAuthentication() {
		try {
			const userResponse = await usersCurrentUserUserMeGet()
			if (userResponse) {
				localStorage.setItem('me', JSON.stringify(userResponse))
				isAuthenticated.set(true)
			}
		} catch {
			localStorage.removeItem('me')
			isAuthenticated.set(false)
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			checkAuthentication()
		}
	})
</script>

<NavBar />

<main>
	<slot />
</main>

<Footer />

<style>
	:global(body) {
		font-family:
			-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
			'Noto Color Emoji';
		background-color: #000000;
		color: #ffffff;
	}

	main {
		position: relative;
	}
</style>
