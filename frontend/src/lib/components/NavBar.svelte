<script lang="ts">
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button, Input } from 'flowbite-svelte'
	import { SearchOutline } from 'flowbite-svelte-icons'
	import LoginButton from '$lib/components/LoginButton.svelte'
</script>

<Navbar class="px-2 sm:px-4 py-2.5 fixed w-full z-20 top-0 start-0 border-b ">
	<NavBrand href="/home">
		<img src="/src/assets/logo.png" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>Sessionary</span
		>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/favorites">즐겨찾기</NavLi>
		<NavLi href="/folder">나의 폴더</NavLi>
	</NavUl>
	<div class="flex">
		<Button
			color="none"
			data-collapse-toggle="mobile-menu-3"
			aria-controls="mobile-menu-3"
			aria-expanded="false"
			class="md:hidden text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 me-1"
		>
			<SearchOutline class="w-5 h-5" />
		</Button>
		<div class="hidden relative md:block">
			<div class="flex absolute inset-y-0 start-0 items-center ps-3 pointer-events-none">
				<SearchOutline class="w-4 h-4" />
			</div>
			<Input id="search-navbar" class="ps-10" placeholder="Search..." />
		</div>
		<NavHamburger />
	</div>
	<LoginButton />
</Navbar>
