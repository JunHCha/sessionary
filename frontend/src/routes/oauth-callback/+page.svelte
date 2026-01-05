<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { setIsAuthenticated } from '$lib/features/auth'
	import {
		oauthGoogleRedisCallbackUserOauthGoogleCallbackGet,
		usersCurrentUserUserMeGet,
		waitForApiInit
	} from '$lib/api'
	import { Spinner } from 'flowbite-svelte'

	let { data }: { data: { props: { code?: string; state?: string; error?: string } } } = $props()

	onMount(async () => {
		await waitForApiInit()

		const code = data.props.code
		const state = data.props.state
		const error = data.props.error

		if (error || !code || !state) {
			console.error('OAuth2 error:', { error, code, state })
			alert('로그인 중 오류가 발생했습니다. 다시 시도해 주세요.')
			goto('/home')
			return
		}

		try {
			await oauthGoogleRedisCallbackUserOauthGoogleCallbackGet({ code, state })

			if (typeof window !== 'undefined') {
				const userResponse = await usersCurrentUserUserMeGet()
				localStorage.setItem('me', JSON.stringify(userResponse))
				setIsAuthenticated(true)
				goto('/home')
			}
		} catch (err) {
			console.error('Callback error:', err)
			goto('/not-found')
		}
	})
</script>

<main class="flex flex-col items-center justify-center h-screen">
	<h1 class="text-2xl font-bold m-8">로그인 중...</h1>
	<Spinner />
</main>
