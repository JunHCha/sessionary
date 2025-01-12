<script context="module" lang="ts">
	import { isAuthenticated } from '$lib/stores/auth'
	export const load = async ({ data }: { data: { env: { PUBLIC_API_BASE_URL: string } } }) => {
		return { data }
	}
</script>

<script lang="ts">
	import '../app.pcss'

	export let data: {
		env: {
			PUBLIC_API_BASE_URL: string
		}
	}
	import { onMount } from 'svelte'
	import { OpenAPI } from '$lib/client'
	import NavBar from '../lib/components/NavBar.svelte'
	import { usersCurrentUserUserMeGet } from '$lib/client'

	OpenAPI.BASE = data.env.PUBLIC_API_BASE_URL
	OpenAPI.WITH_CREDENTIALS = true
	OpenAPI.interceptors.request.use((request) => {
		request.withCredentials = true
		return request
	})

	async function checkAuthentication() {
		try {
			const userResponse = await usersCurrentUserUserMeGet()
			if (userResponse) {
				localStorage.setItem('me', JSON.stringify(userResponse))
				isAuthenticated.set(true)
			}
		} catch (error) {
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

<style>
	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
			'Noto Color Emoji';
	}

	main {
		padding: 1rem;
		position: relative;
		top: 60px;
	}
</style>
