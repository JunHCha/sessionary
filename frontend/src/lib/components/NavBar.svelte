<script lang="ts">
	import RouteButton from './RouteButton.svelte'
	import LoginButton from './LoginButton.svelte'
	import SearchButton from './SearchButton.svelte'
	import Logo from './Logo.svelte'
</script>

<nav>
	<div class="left-group">
		<Logo />
		<RouteButton route="/favorites" label="즐겨찾기" />
		<RouteButton route="/folder" label="나의 폴더" />
	</div>
	<div class="right-group">
		<SearchButton />
		<LoginButton />
	</div>
</nav>

<style>
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		background-color: #f0f0f0;
	}

	.left-group,
	.right-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
</style>
