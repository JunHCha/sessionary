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
	class="w-full h-[clamp(3rem,5vh,5rem)] px-[clamp(2rem,5vw,5.25rem)] flex items-center bg-[#0C0C0C] opacity-95 fixed z-50 transition-all duration-300"
	class:minimal={isScrolled}
	data-testid="navbar"
>
	<a
		href="/home"
		class="h-full w-[clamp(8rem,13vw,13.4rem)] flex items-center justify-start pl-0 pr-[clamp(0.5rem,0.6vw,0.6rem)]"
	>
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
			class="h-[clamp(3rem,5vh,5rem)] w-[clamp(6rem,8.75vw,8.75rem)] flex items-center justify-center p-[clamp(0.5rem,0.6vw,0.6rem)] text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			즐겨찾기
		</a>
		<a
			href="/folder"
			class="h-[clamp(3rem,5vh,5rem)] w-[clamp(6rem,8.75vw,8.75rem)] flex items-center justify-center p-[clamp(0.5rem,0.6vw,0.6rem)] text-[clamp(0.9rem,1.3vw,1.3rem)] font-pretendard font-bold leading-[clamp(1.3rem,2vw,2rem)] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			나의폴더
		</a>
	</div>
	<div class="ml-auto flex items-center">
		<div
			class="h-[clamp(3rem,5vh,5rem)] min-w-[clamp(4rem,6.25vw,6.25rem)] flex items-center justify-end p-[clamp(0.5rem,0.6vw,0.6rem)] transition-opacity duration-300"
			class:opacity-0={isScrolled}
		>
			<LoginButton />
		</div>
		<button
			class="h-[clamp(3rem,5vh,5rem)] w-[clamp(3rem,5vw,5rem)] flex items-center justify-center"
		>
			<img
				src="images/iconamoon_search-bold.png"
				alt="search"
				class="h-[clamp(1.2rem,1.9vw,1.9rem)] w-[clamp(1.2rem,1.9vw,1.9rem)]"
			/>
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
