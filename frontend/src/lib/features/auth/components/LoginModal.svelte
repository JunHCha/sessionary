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

	async function handleLogin() {
		try {
			saveRedirectUrl(redirectUrl)
			const response = await oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet({
				scopes: []
			})
			const { authorization_url } = response
			window.location.href = authorization_url
		} catch (error) {
			console.error('Login error:', error)
		}
	}
</script>

<Modal bind:open size="xs" autoclose={false} class="w-full">
	<div class="flex flex-col items-center space-y-6 p-4">
		<h3 class="text-xl font-bold text-white">{message}</h3>

		<Button
			type="button"
			class="w-full bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-white font-bold py-3 rounded-lg"
			onclick={handleLogin}
		>
			Google로 로그인
		</Button>
	</div>
</Modal>

<style>
	:global(.modal-container) {
		background-color: #0c0c0c !important;
	}
</style>
