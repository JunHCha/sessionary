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
	import { Modal } from '$lib/components'
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
	<div class="flex flex-col items-center gap-6 p-8">
		<h3 class="text-xl font-bold text-[#e5e5e5]">{message}</h3>

		{#if errorMessage}
			<p class="text-red-500 text-sm">{errorMessage}</p>
		{/if}

		<button
			type="button"
			class="w-full bg-[#FF5C16] hover:bg-[#FF5C16]/90 text-[#e5e5e5] font-bold py-3 rounded-lg transition-colors"
			onclick={handleLogin}
		>
			Sign in with Google
		</button>
	</div>
</Modal>

