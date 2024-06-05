<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/stores/auth';
	import {
		oauthGoogleRedisCallbackUserOauthGoogleCallbackGet,
		usersCurrentUserUserMeGet
	} from '$lib/client/services.gen';

	export let data: {
		props: { code: string | undefined; state: string | undefined; error: string | undefined };
	}; // data의 타입을 명시

	onMount(async () => {
		let code = data.props.code;
		let state = data.props.state;
		let error = data.props.error;
		if (error) {
			console.error('OAuth2 error:', error);
			goto('/login');
			return;
		}

		try {
			const response = (await oauthGoogleRedisCallbackUserOauthGoogleCallbackGet({
				code,
				state
			})) as { access_token: string; token_type: string };
			const access_token = response.access_token;

			if (typeof window !== 'undefined') {
				localStorage.setItem('satk', access_token);

				const userResponse = await usersCurrentUserUserMeGet();
				localStorage.setItem('me', JSON.stringify(userResponse));
				isAuthenticated.set(true); // 인증 상태 업데이트

				goto('/home');
			}
		} catch (error) {
			console.error('Callback error:', error);
			goto('/login');
		}
	});
</script>

<main>
	<h1>로그인 중...</h1>
</main>

<style>
	main {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		background-color: lavender;
	}
</style>
