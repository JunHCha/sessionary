<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { isAuthenticated } from '$lib/stores/auth'
	import {
		oauthGoogleRedisCallbackUserOauthGoogleCallbackGet,
		usersCurrentUserUserMeGet
	} from '$lib/client/services.gen'
	import { Spinner } from 'flowbite-svelte'

	export let data: {
		props: { code?: string; state?: string; error?: string }
	}

	onMount(async () => {
		let code = data.props.code
		let state = data.props.state
		let error = data.props.error
		if (error || !code || !state) {
			console.error('OAuth2 error:', { error, code, state })
			alert('로그인 중 오류가 발생했습니다. 다시 시도해 주세요.')
			goto('/home')
			return
		}

		try {
			await oauthGoogleRedisCallbackUserOauthGoogleCallbackGet({
				code,
				state
			})

			if (typeof window !== 'undefined') {
				const userResponse = await usersCurrentUserUserMeGet()
				localStorage.setItem('me', JSON.stringify(userResponse))
				isAuthenticated.set(true)

				goto('/home')
			}
		} catch (error) {
			console.error('Callback error:', error)
			goto('/not-found')
		}
	})
</script>

<main class="flex flex-col items-center justify-center h-screen">
	<h1 class="text-2xl font-bold m-8">로그인 중...</h1>
	<Spinner />
</main>
