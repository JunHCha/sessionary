<script lang="ts">
	import { onMount } from 'svelte'
	import { LoginButton } from '$lib/features/auth'

	let isScrolled = false

	onMount(() => {
		const handleScroll = () => {
			const heroSection = document.querySelector('.hero-section')
			if (heroSection) {
				const heroMiddle =
					heroSection.getBoundingClientRect().top +
					heroSection.getBoundingClientRect().height / 3
				isScrolled = heroMiddle < 0
			}
		}

		window.addEventListener('scroll', handleScroll)
		return () => {
			window.removeEventListener('scroll', handleScroll)
		}
	})
</script>

<div
	class="w-full h-20 px-20 py-2 flex bg-black/60 items-center fixed z-50 transition-all duration-300"
	class:minimal="{isScrolled}"
	data-testid="navbar"
>
	<img
		src="images/logo.png"
		srcset="images/logo@2x.png 2x, images/logo@3x.png 3x"
		class="w-[220px] h-[63.1px] mr-[69px] object-contain transition-opacity duration-300"
		class:opacity-0="{isScrolled}"
		alt="Sessionary Logo"
	/>
	<div class="flex gap-[60px] transition-opacity duration-300" class:opacity-0="{isScrolled}">
		<span class="text-lg font-pretendard font-bold uppercase text-white">즐겨찾기</span>
		<span class="text-lg font-pretendard font-bold uppercase text-white">나의폴더</span>
	</div>
	<div class="ml-auto flex gap-10">
		<div class="transition-opacity duration-300" class:opacity-0="{isScrolled}">
			<LoginButton />
		</div>
		<button class="w-10 h-10">
			<img src="images/iconamoon_search-bold.png" alt="search" />
		</button>
	</div>
</div>

<style>
	.minimal {
		height: 3rem;
		padding-top: 0.5rem;
		padding-bottom: 0.5rem;
		background-color: rgba(0, 0, 0, 0);
	}
</style>
