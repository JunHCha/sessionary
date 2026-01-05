<script lang="ts">
	import { goto } from '$app/navigation'
	import { isAuthenticated } from '../stores/auth.svelte'
	import { Button, Modal } from 'flowbite-svelte'
	import {
		oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet,
		authRedisLogoutUserAuthLogoutPost
	} from '$lib/api/client'

	let formModal = false

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

	async function handleLogout() {
		try {
			await authRedisLogoutUserAuthLogoutPost()
			localStorage.removeItem('me')
			isAuthenticated.set(false)
			goto('/home')
		} catch (error) {
			console.error('Logout error:', error)
		}
	}
</script>

{#if $isAuthenticated}
	<button
		on:click={handleLogout}
		class="text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap text-right"
	>
		로그아웃
	</button>
{:else}
	<button
		on:click={() => (formModal = true)}
		class="text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap text-right"
		data-testid="login-button"
	>
		로그인
	</button>
{/if}

<Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6" action="#">
		<h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
			Sign in to our platform
		</h3>

		<Button type="submit" class="w-full" onclick={handleLogin}>Signup with Google</Button>
	</form>
</Modal>
