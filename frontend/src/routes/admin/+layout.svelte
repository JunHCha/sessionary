<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { page } from '$app/stores'
	import { waitForApiInit, usersCurrentUserUserMeGet } from '$lib/api'
	import { setCurrentUser, useAuth } from '$lib/features/auth'
	import type { Snippet } from 'svelte'

	let { children }: { children: Snippet } = $props()
	let checked = $state(false)
	let mobileOpen = $state(false)
	const auth = useAuth()

	const navItems = [
		{ href: '/admin', label: '대시보드', icon: 'grid', exact: true },
		{ href: '/admin/lectures', label: '렉처', icon: 'stack', exact: false },
		{ href: '/admin/curation', label: '홈 큐레이션', icon: 'spark', exact: false }
	]

	const currentPath = $derived($page.url.pathname)

	function isActive(item: { href: string; exact: boolean }): boolean {
		if (item.exact) return currentPath === item.href
		return currentPath === item.href || currentPath.startsWith(item.href + '/')
	}

	onMount(async () => {
		await waitForApiInit()
		try {
			const me = await usersCurrentUserUserMeGet()
			setCurrentUser(me)
		} catch {
			setCurrentUser(null)
		}
		if (!auth.isAdmin) {
			goto('/home', { replaceState: true })
			return
		}
		checked = true
	})
</script>

{#snippet navIcon(name: string)}
	<svg
		class="h-[18px] w-[18px] shrink-0"
		viewBox="0 0 24 24"
		fill="none"
		stroke="currentColor"
		stroke-width="1.8"
		stroke-linecap="round"
		stroke-linejoin="round"
	>
		{#if name === 'grid'}
			<rect x="3" y="3" width="7" height="7" rx="1.5" />
			<rect x="14" y="3" width="7" height="7" rx="1.5" />
			<rect x="3" y="14" width="7" height="7" rx="1.5" />
			<rect x="14" y="14" width="7" height="7" rx="1.5" />
		{:else if name === 'stack'}
			<path d="M12 3 3 7.5 12 12l9-4.5L12 3Z" />
			<path d="m3 12 9 4.5L21 12" />
			<path d="m3 16.5 9 4.5 9-4.5" />
		{:else if name === 'spark'}
			<path d="M12 3v4M12 17v4M3 12h4M17 12h4" />
			<path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z" />
		{/if}
	</svg>
{/snippet}

{#snippet navLinks(onNavigate: () => void)}
	{#each navItems as item (item.href)}
		{@const active = isActive(item)}
		<a
			href={item.href}
			onclick={onNavigate}
			aria-current={active ? 'page' : undefined}
			class="group relative flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-[14px] font-pretendard font-semibold tracking-[-0.01em] transition-colors duration-150
				{active ? 'bg-[#FF5C16]/10 text-white' : 'text-[#9a9a9a] hover:bg-white/[0.04] hover:text-white'}"
		>
			<span
				class="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-[#FF5C16] transition-opacity duration-150
					{active ? 'opacity-100' : 'opacity-0'}"
			></span>
			<span class={active ? 'text-[#FF5C16]' : 'text-[#6f6f6f] group-hover:text-[#bdbdbd]'}>
				{@render navIcon(item.icon)}
			</span>
			{item.label}
		</a>
	{/each}
{/snippet}

{#if checked}
	<div
		class="min-h-screen bg-[#0C0C0C] text-white font-pretendard md:flex"
		data-testid="admin-shell"
	>
		<!-- 모바일 상단바 -->
		<header
			class="sticky top-0 z-40 flex items-center justify-between border-b border-white/[0.06] bg-[#0C0C0C]/95 px-5 py-3.5 backdrop-blur md:hidden"
		>
			<div class="flex items-center gap-2.5">
				<span class="h-5 w-[3px] rounded-full bg-[#FF5C16]"></span>
				<span class="text-[15px] font-bold tracking-[-0.02em]">Sessionary Admin</span>
			</div>
			<button
				type="button"
				aria-label="메뉴"
				aria-expanded={mobileOpen}
				onclick={() => (mobileOpen = !mobileOpen)}
				class="flex h-9 w-9 items-center justify-center rounded-lg text-[#bdbdbd] hover:bg-white/[0.05] hover:text-white"
			>
				<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					{#if mobileOpen}
						<path stroke-width="2" stroke-linecap="round" d="M6 6l12 12M6 18 18 6" />
					{:else}
						<path stroke-width="2" stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16" />
					{/if}
				</svg>
			</button>
		</header>

		{#if mobileOpen}
			<nav
				class="flex flex-col gap-1 border-b border-white/[0.06] bg-[#0e0e0e] px-4 py-3 md:hidden"
			>
				{@render navLinks(() => (mobileOpen = false))}
				<a
					href="/home"
					onclick={() => (mobileOpen = false)}
					class="mt-1 flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-[13px] font-medium text-[#7a7a7a] hover:bg-white/[0.04] hover:text-white"
				>
					← 사이트로 돌아가기
				</a>
			</nav>
		{/if}

		<!-- 데스크탑 사이드바 -->
		<aside
			class="sticky top-0 hidden h-screen w-[248px] shrink-0 flex-col border-r border-white/[0.06] bg-[#0b0b0b] px-4 py-6 md:flex"
		>
			<a href="/admin" class="mb-8 flex items-center gap-2.5 px-2">
				<span class="flex h-8 w-8 items-center justify-center rounded-lg bg-[#FF5C16]/15">
					<span class="h-3.5 w-[3px] rounded-full bg-[#FF5C16]"></span>
				</span>
				<div class="flex flex-col leading-tight">
					<span class="text-[15px] font-bold tracking-[-0.02em]">Sessionary</span>
					<span class="text-[11px] font-medium tracking-[0.12em] text-[#FF5C16]"
						>ADMIN</span
					>
				</div>
			</a>

			<nav class="flex flex-1 flex-col gap-1">
				{@render navLinks(() => {})}
			</nav>

			<div class="mt-6 flex flex-col gap-3 border-t border-white/[0.06] pt-5">
				<div class="flex items-center gap-2.5 px-2">
					<span
						class="flex h-8 w-8 items-center justify-center rounded-full bg-white/[0.06] text-[12px] font-bold text-[#FF5C16]"
					>
						{(auth.user?.nickname ?? 'A').slice(0, 1).toUpperCase()}
					</span>
					<div class="flex min-w-0 flex-col leading-tight">
						<span class="truncate text-[13px] font-semibold"
							>{auth.user?.nickname ?? '관리자'}</span
						>
						<span class="truncate text-[11px] text-[#6f6f6f]"
							>{auth.user?.email ?? ''}</span
						>
					</div>
				</div>
				<a
					href="/home"
					class="flex items-center gap-2 rounded-lg px-2 py-2 text-[12.5px] font-medium text-[#7a7a7a] transition-colors hover:bg-white/[0.04] hover:text-white"
				>
					<svg
						class="h-4 w-4"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.8"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M19 12H5M11 6l-6 6 6 6" />
					</svg>
					사이트로 돌아가기
				</a>
			</div>
		</aside>

		<!-- 콘텐츠 -->
		<main class="min-w-0 flex-1 px-5 py-7 sm:px-8 sm:py-10 lg:px-12">
			<div class="mx-auto w-full max-w-[1080px]">
				{@render children()}
			</div>
		</main>
	</div>
{:else}
	<div class="min-h-screen bg-black" data-testid="admin-loading"></div>
{/if}
