<script lang="ts" module>
	// 테스트를 위해 export하는 유틸리티 함수들
	export function getDefaultMessage(): string {
		return '로그인이 필요합니다'
	}

	export function getDefaultRedirectUrl(): string {
		return '/home'
	}

	export function saveRedirectUrl(url: string): void {
		if (typeof sessionStorage !== 'undefined') {
			sessionStorage.setItem('redirectUrl', url)
		}
	}
</script>

<script lang="ts">
	import { Modal, Button } from 'flowbite-svelte'
	import { oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet } from '$lib/api/client'

	interface Props {
		open: boolean
		message?: string
		redirectUrl?: string
	}

	let {
		open = $bindable(),
		message = getDefaultMessage(),
		redirectUrl = getDefaultRedirectUrl()
	}: Props = $props()

	let errorMessage = $state('')

	async function handleLogin() {
		errorMessage = ''
		try {
			saveRedirectUrl(redirectUrl)
			const response = await oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet({
				scopes: []
			})
			const { authorization_url } = response
			window.location.href = authorization_url
		} catch (error) {
			console.error('Login error:', error)
			errorMessage = '로그인 처리 중 오류가 발생했습니다. 다시 시도해 주세요.'
		}
	}
</script>

<Modal bind:open size="xs" autoclose={false} class="modal-dark">
	<div class="flex flex-col items-center gap-6 p-6">
		<h3 class="text-xl font-bold text-[#e5e5e5]">{message}</h3>

		{#if errorMessage}
			<p class="text-red-500 text-sm">{errorMessage}</p>
		{/if}

		<Button
			type="button"
			class="w-full bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-[#e5e5e5] font-bold py-3 rounded-lg"
			onclick={handleLogin}
		>
			Sign in with Google
		</Button>
	</div>
</Modal>

<style>
	:global(.modal-dark) {
		background: linear-gradient(to right, #1a1410, #0c0c0c) !important;
		border: 1px solid #ff5c16;
		box-shadow: 0px 20px 25px -5px rgba(255, 92, 22, 0.2), 0px 8px 10px -6px rgba(255, 92, 22, 0.2);
		border-radius: 0.75rem;
	}

	:global(.modal-dark > div) {
		background: linear-gradient(to right, #1a1410, #0c0c0c) !important;
		border-radius: 0.75rem;
	}

	:global([data-modal-backdrop]),
	:global(.fixed.inset-0.z-40),
	:global(body > .fixed.inset-0) {
		background-color: rgba(0, 0, 0, 0.85) !important;
		backdrop-filter: blur(2px);
	}
</style>
