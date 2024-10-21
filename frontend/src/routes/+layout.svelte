<script context="module" lang="ts">
	import { isAuthenticated } from '$lib/stores/auth'
	export const load = async ({ data }: import('./$types').LayoutServerLoad) => {
		return data
	}
</script>

<script lang="ts">
	export let data: {
		env: {
			PUBLIC_API_BASE_URL: string
		}
	}
	import { onMount } from 'svelte'
	import { OpenAPI } from '$lib/client'
	import NavBar from '$lib/components/NavBar.svelte'

	OpenAPI.BASE = data.env.PUBLIC_API_BASE_URL
	OpenAPI.interceptors.request.use((request) => {
		let token = localStorage.getItem('satk')
		if (token) {
			request.headers = request.headers ?? {}
			request.headers['Authorization'] = `Bearer ${token}`
		}
		return request
	})

	function checkAuthentication() {
		const token = localStorage.getItem('satk')
		const user = localStorage.getItem('me')
		if (token && user) isAuthenticated.set(true)
		else isAuthenticated.set(false)
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
	main {
		padding: 1rem;
	}
</style>
