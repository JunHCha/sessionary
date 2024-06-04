<script lang="ts">
	import { OpenAPI } from '$lib/client';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import {
		oauthGoogleRedisCallbackUserOauthGoogleCallbackGet,
		usersCurrentUserUserMeGet
	} from '$lib/client/services.gen';

	OpenAPI.BASE = 'http://localhost:8000';
	OpenAPI.interceptors.request.use((request) => {
		request.headers['Authorization'] = `Bearer ${localStorage.getItem('satk')}`;
		// TODO: fix type

		return request;
	});

	export let data: any;
	let code = data.props.code;
	let state = data.props.state;
	let error = data.props.error;

	onMount(async () => {
		if (error) {
			console.error('OAuth2 error:', error);
			goto('/login');
			return;
		}

		try {
			const response = await oauthGoogleRedisCallbackUserOauthGoogleCallbackGet({ code, state });
			console.log('Callback response:', response);
			const { access_token } = response;

			if (typeof window !== 'undefined') {
				localStorage.setItem('satk', access_token);

				// 토큰 유효성 검증 및 사용자 정보 가져오기
				const userResponse = await usersCurrentUserUserMeGet();
				localStorage.setItem('me', JSON.stringify(userResponse));

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
