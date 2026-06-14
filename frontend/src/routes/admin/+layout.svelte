<script lang="ts">
	import { onMount } from 'svelte'
	import { goto } from '$app/navigation'
	import { waitForApiInit, usersCurrentUserUserMeGet } from '$lib/api'
	import { setCurrentUser, useAuth } from '$lib/features/auth'
	import type { Snippet } from 'svelte'

	let { children }: { children: Snippet } = $props()
	let checked = $state(false)
	const auth = useAuth()

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

{#if checked}
	<div
		class="min-h-screen bg-black text-white px-6 py-20 max-w-[1024px] mx-auto"
		data-testid="admin-shell"
	>
		<nav class="flex gap-4 mb-8 text-sm">
			<a href="/admin/lectures" class="hover:text-[#FF5C16]">렉처</a>
			<a href="/admin/curation" class="hover:text-[#FF5C16]">홈 큐레이션</a>
		</nav>
		{@render children()}
	</div>
{:else}
	<div class="min-h-screen bg-black" data-testid="admin-loading"></div>
{/if}
