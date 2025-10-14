<script context="module" lang="ts">
	import { isAuthenticated } from '$lib/stores/auth'
	export const load = async ({ data }: { data: { env: { PUBLIC_API_BASE_URL: string } } }) => {
		return { data }
	}
</script>

<script lang="ts">
	import '../app.pcss'

	export let data: {
		env: {
			PUBLIC_API_BASE_URL: string
		}
	}
	import { onMount } from 'svelte'
	import { OpenAPI } from '$lib/client'
	import NavBar from '../lib/components/NavBar.svelte'
	import { usersCurrentUserUserMeGet } from '$lib/client'

	OpenAPI.BASE = data.env.PUBLIC_API_BASE_URL
	OpenAPI.WITH_CREDENTIALS = true
	OpenAPI.interceptors.request.use((request) => {
		request.withCredentials = true
		return request
	})

	async function checkAuthentication() {
		try {
			const userResponse = await usersCurrentUserUserMeGet()
			if (userResponse) {
				localStorage.setItem('me', JSON.stringify(userResponse))
				isAuthenticated.set(true)
			}
		} catch (error) {
			localStorage.removeItem('me')
			isAuthenticated.set(false)
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			checkAuthentication()
		}
	})
</script>

<NavBar />

<main>
	<slot />
</main>

<footer
	class="w-[1920px] h-[161px] mt-[761px] px-[80px] pt-[35px] pb-[14px] flex items-start mb-[5rem]"
>
	<img
		src="images/logo.png"
		srcset="images/logo@2x.png 2x,
                images/logo@3x.png 3x"
		class="w-[220px] h-[63.1px] object-contain opacity-50"
		alt="Sessionary Logo"
	/>
	<span
		class="w-[646px] h-[112px] mx-[38px] mr-[413px] font-pretendard text-base font-medium leading-[1.75] tracking-[-0.32px] text-left text-[#656565]"
	>
		대표: 홍길동
		<span class="text-sm tracking-[-0.28px]">ㅣ</span>
		사업자등록번호: 000-00-00000
		<span class="text-sm tracking-[-0.28px]">ㅣ</span>
		통신판매업신고번호: 제0000-서울00-0000호 <br />
		주소: 서울특별시 ㅇㅇ구 ㅇㅇ국로 00, 우편번호 00000
		<span class="text-sm tracking-[-0.28px]">ㅣ</span>
		고객센터: 0000-0000<br />
		대표 메일: 0000@sessionary.com
		<span class="text-sm tracking-[-0.28px]">ㅣ</span>
		제휴 문의: 0000@sessionary.com<br />
		호스팅: ㅇㅇㅇㅇㅇ
	</span>
</footer>

<style>
	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
			'Noto Color Emoji';
		background-color: #000000;
		color: #ffffff;
	}

	main {
		position: relative;
	}
</style>
