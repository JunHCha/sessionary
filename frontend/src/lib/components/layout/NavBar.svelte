<script lang="ts">
	import { LoginButton } from '$lib/features/auth'
	import { onMount } from 'svelte'

	let isScrolled = $state(false)
	let isVisible = $state(true)
	let menuOpen = $state(false)
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
	class="w-full min-w-[390px] h-[50px] bg-[#0C0C0C] fixed z-50 transition-all duration-300"
	class:minimal={isScrolled}
	class:opacity-95={isVisible}
	class:opacity-0={!isVisible}
	class:-translate-y-full={!isVisible}
	class:pointer-events-none={!isVisible}
	data-testid="navbar"
>
	<div class="w-full max-w-[1280px] mx-auto px-[40px] h-full flex items-center">
		<a href="/home" class="h-full w-[134px] flex items-center justify-start">
			<img
				src="/images/logo.png"
				srcset="/images/logo@2x.png 2x"
				class="h-full w-full object-contain transition-opacity duration-300"
				alt="Sessionary Logo"
			/>
		</a>
		<!-- 데스크탑 메뉴 (md 이상) -->
		<div class="hidden md:flex gap-0">
			<a
				href="/favorites"
				class="h-[50px] w-[88px] flex items-center justify-center text-[13px] font-pretendard font-bold leading-[20px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			>
				즐겨찾기
			</a>
			<a
				href="/folder"
				class="h-[50px] w-[88px] flex items-center justify-center text-[13px] font-pretendard font-bold leading-[20px] tracking-[-0.02em] text-[#F5F5F5] whitespace-nowrap transition-opacity duration-300"
			>
				나의폴더
			</a>
		</div>
		<div class="ml-auto hidden md:flex items-center">
			<div class="h-[50px] flex items-center justify-end transition-opacity duration-300">
				<LoginButton />
			</div>
			<button
				aria-label="검색"
				type="button"
				class="h-[50px] w-[50px] flex items-center justify-center transition-opacity duration-300"
			>
				<img
					src="/images/iconamoon_search-bold.png"
					alt="search"
					class="h-[19px] w-[19px]"
				/>
			</button>
		</div>

		<!-- 햄버거 (md 미만) -->
		<button
			type="button"
			aria-label="메뉴"
			aria-expanded={menuOpen}
			onclick={() => (menuOpen = !menuOpen)}
			class="ml-auto md:hidden h-[50px] w-[50px] flex items-center justify-center text-[#F5F5F5]"
		>
			<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				{#if menuOpen}
					<path stroke-width="2" stroke-linecap="round" d="M6 6l12 12M6 18 18 6" />
				{:else}
					<path stroke-width="2" stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16" />
				{/if}
			</svg>
		</button>
	</div>

	<!-- 모바일 드롭다운 메뉴 (md 미만, 햄버거 토글) -->
	{#if menuOpen}
		<div
			class="md:hidden absolute top-full inset-x-0 bg-[#0C0C0C] border-t border-[#1a1a1a] flex flex-col py-1"
		>
			<a
				href="/favorites"
				onclick={() => (menuOpen = false)}
				class="px-[40px] py-3 text-[14px] font-pretendard font-bold text-[#F5F5F5]"
				>즐겨찾기</a
			>
			<a
				href="/folder"
				onclick={() => (menuOpen = false)}
				class="px-[40px] py-3 text-[14px] font-pretendard font-bold text-[#F5F5F5]"
				>나의폴더</a
			>
			<div class="px-[40px] py-3 border-t border-[#1a1a1a] flex items-center justify-between">
				<LoginButton />
				<button aria-label="검색" type="button" class="flex items-center">
					<img
						src="/images/iconamoon_search-bold.png"
						alt="search"
						class="h-[19px] w-[19px]"
					/>
				</button>
			</div>
		</div>
	{/if}
</div>

<style>
	.minimal {
		height: 3rem;
		padding-top: 0.5rem;
		padding-bottom: 0.5rem;
		background-color: rgba(0, 0, 0, 0);
	}
</style>
