<script lang="ts">
	const tiles = [
		{
			href: '/admin/lectures',
			title: '렉처 관리',
			desc: '렉처를 생성하고 속성·레슨을 편집합니다',
			icon: 'stack'
		},
		{
			href: '/admin/curation',
			title: '홈 큐레이션',
			desc: '홈 화면에 노출할 렉처를 섹션별로 선정합니다',
			icon: 'spark'
		}
	]
</script>

<div data-testid="admin-hub" class="flex flex-col gap-9 font-pretendard">
	<header class="flex flex-col gap-2">
		<span class="text-[12px] font-semibold uppercase tracking-[0.18em] text-[#FF5C16]">
			Dashboard
		</span>
		<h1 class="text-[28px] font-bold leading-tight tracking-[-0.02em] sm:text-[32px]">
			관리자
		</h1>
		<p class="text-[14px] text-[#848484]">콘텐츠와 홈 노출을 한곳에서 관리하세요.</p>
	</header>

	<div class="grid gap-4 sm:grid-cols-2">
		{#each tiles as tile (tile.href)}
			<a
				href={tile.href}
				class="group relative flex flex-col gap-4 overflow-hidden rounded-2xl border border-white/[0.07] bg-[#141414] p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-[#FF5C16]/50 hover:bg-[#171717]"
			>
				<span
					class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[#FF5C16]/60 to-transparent opacity-0 transition-opacity duration-200 group-hover:opacity-100"
				></span>
				<span
					class="flex h-11 w-11 items-center justify-center rounded-xl bg-[#FF5C16]/12 text-[#FF5C16]"
				>
					<svg
						class="h-[22px] w-[22px]"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.8"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						{#if tile.icon === 'stack'}
							<path d="M12 3 3 7.5 12 12l9-4.5L12 3Z" />
							<path d="m3 12 9 4.5L21 12" />
							<path d="m3 16.5 9 4.5 9-4.5" />
						{:else}
							<path d="M12 3v4M12 17v4M3 12h4M17 12h4" />
							<path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z" />
						{/if}
					</svg>
				</span>
				<div class="flex flex-col gap-1.5">
					<h2 class="text-[18px] font-bold tracking-[-0.01em]">{tile.title}</h2>
					<p class="text-[13.5px] leading-relaxed text-[#848484]">{tile.desc}</p>
				</div>
				<span
					class="mt-1 inline-flex items-center gap-1.5 text-[13px] font-semibold text-[#848484] transition-colors group-hover:text-[#FF5C16]"
				>
					바로가기
					<svg
						class="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M5 12h14M13 6l6 6-6 6" />
					</svg>
				</span>
			</a>
		{/each}
	</div>
</div>
