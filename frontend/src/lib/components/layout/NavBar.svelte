<script lang="ts">
	import { LoginButton } from '$lib/features/auth'
	import { onMount } from 'svelte'

	let isScrolled = $state(false)
	let isVisible = $state(true)
	let lastScrollY = $state(0)
	let hideTimer: ReturnType<typeof setTimeout> | null = null

	const SCROLL_THRESHOLD = 300
	const HIDE_DELAY = 2000

	function getScrollY() {
		const mainElement = document.querySelector('main.overflow-y-scroll')
		return mainElement
			? mainElement.scrollTop
			: window.scrollY || document.documentElement.scrollTop
	}

	function clearHideTimer() {
		if (hideTimer) {
			clearTimeout(hideTimer)
			hideTimer = null
		}
	}

	function scheduleHide() {
		clearHideTimer()
		hideTimer = setTimeout(() => {
			isVisible = false
			hideTimer = null
		}, HIDE_DELAY)
	}

	function handleScroll() {
		const scrollY = getScrollY()
		const scrolledPastThreshold = scrollY > SCROLL_THRESHOLD
		const scrollingDown = scrollY > lastScrollY
		const scrollingUp = scrollY < lastScrollY

		isScrolled = scrolledPastThreshold

		if (scrollingDown && scrolledPastThreshold) {
			clearHideTimer()
			isVisible = false
		} else if (scrollingUp) {
			clearHideTimer()
			isVisible = true
			if (scrolledPastThreshold) {
				scheduleHide()
			}
		}

		lastScrollY = scrollY
	}

	onMount(() => {
		const mainElement = document.querySelector('main.overflow-y-scroll')
		const scrollElement = mainElement || window

		scrollElement.addEventListener('scroll', handleScroll, { passive: true })
		handleScroll()

		return () => {
			scrollElement.removeEventListener('scroll', handleScroll)
			clearHideTimer()
		}
	})
</script>

<div
	class="w-full h-[clamp(3rem,5vh,5rem)] bg-[#0C0C0C] fixed z-50 transition-all duration-300"
	class:minimal={isScrolled}
	class:opacity-95={isVisible}
	class:opacity-0={!isVisible}
	class:-translate-y-full={!isVisible}
	class:pointer-events-none={!isVisible}
	data-testid="navbar"
>
	<div class="max-w-[1280px] min-w-[1280px] mx-auto h-full flex items-center px-4">
		<a href="/home" class="h-full w-[134px] flex items-center justify-start">
			<img
				src="/images/logo.png"
				srcset="/images/logo@2x.png 2x, /images/logo@3x.png 3x"
				class="h-full w-full object-contain transition-opacity duration-300"
				alt="Sessionary Logo"
			/>
		</a>
		<div class="flex gap-0">
			<a
				href="/favorites"
				class="h-[clamp(3rem,5vh,5rem)] w-[88px] flex items-center justify-center text-[13px] font-pretendard font-bold leading-[20px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			>
				즐겨찾기
			</a>
			<a
				href="/folder"
				class="h-[clamp(3rem,5vh,5rem)] w-[88px] flex items-center justify-center text-[13px] font-pretendard font-bold leading-[20px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			>
				나의폴더
			</a>
		</div>
		<div class="ml-auto flex items-center">
			<div class="h-[clamp(3rem,5vh,5rem)] flex items-center justify-end transition-opacity duration-300">
				<LoginButton />
			</div>
			<button
				aria-label="검색"
				type="button"
				class="h-[clamp(3rem,5vh,5rem)] w-[50px] flex items-center justify-center transition-opacity duration-300"
			>
				<img
					src="/images/iconamoon_search-bold.png"
					alt="search"
					class="h-[19px] w-[19px]"
				/>
			</button>
		</div>
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
