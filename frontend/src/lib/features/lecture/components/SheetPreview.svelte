<script lang="ts">
	let isExpanded = $state(false)
</script>

<div class="flex flex-col gap-4">
	<div class="flex items-center justify-between">
		<h2 class="text-xl font-pretendard font-bold text-white">악보 미리보기</h2>
		<button
			class="text-sm text-brand-primary hover:text-brand-primary/80 transition-colors"
			onclick={() => (isExpanded = !isExpanded)}
		>
			{isExpanded ? '접기' : '전체보기'}
		</button>
	</div>

	<div
		class="relative rounded-xl overflow-hidden bg-surface-card transition-all duration-300"
		class:h-48={!isExpanded}
		class:h-auto={isExpanded}
	>
		<div class="p-6 flex flex-col items-center justify-center min-h-48 gap-4">
			<div class="w-full max-w-md bg-white/5 rounded-lg p-4">
				<div class="grid grid-cols-4 gap-2">
					{#each Array(4) as _, barIdx}
						<div class="flex flex-col gap-1">
							{#each Array(6) as _, stringIdx}
								<div class="flex items-center gap-0.5">
									<span class="w-3 text-[10px] text-content-muted text-right">
										{stringIdx === 0
											? 'e'
											: stringIdx === 1
												? 'B'
												: stringIdx === 2
													? 'G'
													: stringIdx === 3
														? 'D'
														: stringIdx === 4
															? 'A'
															: 'E'}
									</span>
									<div class="flex-1 h-px bg-content-muted/30 relative">
										{#if Math.random() > 0.6}
											<span
												class="absolute -top-1.5 text-[10px] text-brand-primary font-mono"
												style="left: {Math.random() * 80}%"
											>
												{Math.floor(Math.random() * 12)}
											</span>
										{/if}
									</div>
								</div>
							{/each}
						</div>
					{/each}
				</div>
			</div>

			<p class="text-content-muted text-sm">
				전체 악보는 PDF로 다운로드하거나 세션에서 확인하세요
			</p>
		</div>

		{#if !isExpanded}
			<div
				class="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-surface-card to-transparent pointer-events-none"
			></div>
		{/if}
	</div>
</div>
