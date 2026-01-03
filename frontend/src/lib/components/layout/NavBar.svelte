<script lang="ts">
	import { LoginButton } from '$lib/features/auth'

	let isScrolled = $state(false)

	function handleScroll() {
		const heroSection = document.querySelector('.hero-section')
		if (heroSection) {
			const heroMiddle =
				heroSection.getBoundingClientRect().top +
				heroSection.getBoundingClientRect().height / 3
			isScrolled = heroMiddle < 0
		}
	}

	$effect(() => {
		window.addEventListener('scroll', handleScroll)
		return () => {
			window.removeEventListener('scroll', handleScroll)
		}
	})
</script>

<div
	class="w-full h-20 px-[84px] flex items-center bg-[#0C0C0C] opacity-95 fixed z-50 transition-all duration-300"
	class:minimal={isScrolled}
	data-testid="navbar"
>
	<a href="/home" class="h-full w-[214px] flex items-center justify-start pl-0 pr-[10px]">
		<img
			src="images/logo.png"
			srcset="images/logo@2x.png 2x, images/logo@3x.png 3x"
			class="h-full w-full object-contain transition-opacity duration-300"
			class:opacity-0={isScrolled}
			alt="Sessionary Logo"
		/>
	</a>
	<div class="flex gap-0">
		<a
			href="/favorites"
			class="h-[80px] w-[140px] flex items-center justify-center p-[10px] text-[24px] font-pretendard font-bold leading-[36px] tracking-[-0.48px] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			즐겨찾기
		</a>
		<a
			href="/folder"
			class="h-[80px] w-[140px] flex items-center justify-center p-[10px] text-[24px] font-pretendard font-bold leading-[36px] tracking-[-0.48px] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			나의폴더
		</a>
	</div>
	<div class="ml-auto flex items-center">
		<div
			class="h-[80px] min-w-[100px] flex items-center justify-end p-[10px] transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			<LoginButton />
		</div>
		<button class="h-[80px] w-[80px] flex items-center justify-center">
			<img src="images/iconamoon_search-bold.png" alt="search" class="h-[30px] w-[30px]" />
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
