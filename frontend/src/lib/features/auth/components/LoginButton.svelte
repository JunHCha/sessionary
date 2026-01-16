<script lang="ts">
	import { goto } from '$app/navigation'
	import { useAuth, setIsAuthenticated } from '../stores/auth.svelte'
	import { authRedisLogoutUserAuthLogoutPost } from '$lib/api/client'
	import LoginModal from './LoginModal.svelte'

	const auth = useAuth()
	let modalOpen = $state(false)

	async function handleLogout() {
		try {
			await authRedisLogoutUserAuthLogoutPost()
			setIsAuthenticated(false)
			goto('/home')
		} catch (error) {
			console.error('Logout error:', error)
		}
	}
</script>

{#if auth.isAuthenticated}
	<button
		onclick={handleLogout}
		class="text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap text-right"
	>
		로그아웃
	</button>
{:else}
	<button
		onclick={() => (modalOpen = true)}
		class="text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap text-right"
		data-testid="login-button"
	>
		로그인
	</button>
{/if}

<LoginModal bind:open={modalOpen} />
