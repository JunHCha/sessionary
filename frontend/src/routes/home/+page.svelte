<script lang="ts">
	import { isAuthenticated } from '$lib/stores/auth'
</script>

<main>
	{#if $isAuthenticated}
		<h1>환영합니다!</h1>
		<p>이것은 인증된 사용자만 볼 수 있는 콘텐츠입니다.</p>
	{:else}
		<h1>환영합니다!</h1>
		<p>로그인이 필요합니다.</p>
	{/if}
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		background-color: lavender;
	}
</style>
