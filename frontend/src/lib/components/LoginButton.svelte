<script lang="ts">
	import { goto } from '$app/navigation'
	import { isAuthenticated } from '$lib/stores/auth'
	import { Button, Modal } from 'flowbite-svelte'
	import { createEventDispatcher } from 'svelte'
	import { oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet } from '$lib/client/services.gen'

	let formModal = false

	const dispatch = createEventDispatcher()

	async function handleLogin() {
		try {
			const response = await oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet({
				scopes: []
			})
			const { authorization_url } = response
			window.location.href = authorization_url
		} catch (error) {
			console.error('Login error:', error)
		}
	}
	function handleLogout() {
		localStorage.removeItem('satk')
		localStorage.removeItem('me')
		isAuthenticated.set(false)
		goto('/home')
	}
</script>

{#if $isAuthenticated}
	<Button on:click="{handleLogout}">로그아웃</Button>
{:else}
	<Button on:click="{() => (formModal = true)}">로그인/회원가입</Button>
{/if}

<Modal bind:open="{formModal}" size="xs" autoclose="{false}" class="w-full">
	<form class="flex flex-col space-y-6" action="#">
		<h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
			Sign in to our platform
		</h3>

		<Button type="submit" class="w-full1" on:click="{handleLogin}">Signup with Google</Button>
		<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
			Not registered? <a
				href="/"
				class="text-primary-700 hover:underline dark:text-primary-500"
			>
				Create account
			</a>
		</div>
	</form>
</Modal>
