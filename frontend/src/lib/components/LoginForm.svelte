<script>
	import { createEventDispatcher } from 'svelte';
	import { oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet } from '$lib/client/services.gen';
	import { OpenAPI } from '$lib/client';

	OpenAPI.BASE = 'http://localhost:8000';

	const dispatch = createEventDispatcher();

	async function handleLogin() {
		try {
			const response = await oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet({
				scopes: []
			});
			const { authorization_url } = response;
			window.location.href = authorization_url;
		} catch (error) {
			console.error('Login error:', error);
		}
	}
</script>

<div>
	<h2>로그인</h2>
	<button on:click={handleLogin}>Start with Google</button>
</div>

<style>
	div {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	button {
		padding: 1rem 2rem;
		font-size: 1.5rem;
		background-color: #4285f4;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}
</style>
