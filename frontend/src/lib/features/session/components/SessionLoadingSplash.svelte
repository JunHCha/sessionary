<script lang="ts" module>
	export const SPLASH_TESTID = 'session-loading-splash'

	export interface SessionLoadingSplashProps {
		/** 진행 상태 안내 문구 (선택) */
		label?: string
	}

	/**
	 * 기본 Props 값 반환 (테스트용)
	 */
	export function getDefaultProps(): Required<SessionLoadingSplashProps> {
		return {
			label: ''
		}
	}
</script>

<script lang="ts">
	let { label = '' }: SessionLoadingSplashProps = $props()
</script>

<div
	data-testid={SPLASH_TESTID}
	class="splash flex h-[60vh] w-full flex-col items-center justify-center gap-6"
>
	<svg
		class="scene"
		width="280"
		height="220"
		viewBox="0 0 280 220"
		role="img"
		aria-label="기타를 연습하는 소년"
		xmlns="http://www.w3.org/2000/svg"
	>
		<defs>
			<radialGradient id="glow" cx="50%" cy="60%" r="60%">
				<stop offset="0%" stop-color="#FF8A3D" stop-opacity="0.55" />
				<stop offset="55%" stop-color="#FF5C16" stop-opacity="0.18" />
				<stop offset="100%" stop-color="#FF5C16" stop-opacity="0" />
			</radialGradient>
		</defs>

		<!-- 따뜻한 벽난로 불빛 후광 -->
		<ellipse class="glow" cx="205" cy="120" rx="95" ry="80" fill="url(#glow)" />

		<!-- 벽난로 -->
		<rect x="170" y="70" width="80" height="100" rx="6" fill="#1a1a1a" stroke="#333" />
		<rect x="184" y="120" width="52" height="44" rx="4" fill="#0c0c0c" />
		<!-- 장작 -->
		<rect x="190" y="150" width="40" height="8" rx="3" fill="#5a3a22" />
		<rect x="196" y="142" width="30" height="7" rx="3" fill="#6b4329" />
		<!-- 불꽃 (깜빡임) -->
		<path class="flame flame-1" d="M210 152 q-9 -18 0 -30 q9 12 0 30 Z" fill="#FF5C16" />
		<path class="flame flame-2" d="M210 152 q-5 -12 0 -20 q5 8 0 20 Z" fill="#FFB066" />

		<!-- 소파 -->
		<rect x="22" y="138" width="120" height="42" rx="12" fill="#242424" />
		<rect x="14" y="120" width="26" height="58" rx="12" fill="#2c2c2c" />
		<rect x="124" y="120" width="26" height="58" rx="12" fill="#2c2c2c" />

		<!-- 소년 (뒷모습) — 미세한 호흡/연주 모션 -->
		<g class="boy">
			<!-- 머리 -->
			<circle cx="82" cy="92" r="16" fill="#2b2b2b" />
			<!-- 몸통/등 -->
			<path d="M62 150 q20 -42 40 0 Z" fill="#3a3a3a" />
			<!-- 어깨 -->
			<rect x="64" y="104" width="36" height="40" rx="14" fill="#363636" />
			<!-- 기타 넥 -->
			<rect
				class="neck"
				x="96"
				y="118"
				width="52"
				height="7"
				rx="3"
				transform="rotate(-18 96 118)"
				fill="#3d2a18"
			/>
			<!-- 기타 바디 -->
			<ellipse cx="92" cy="138" rx="17" ry="13" fill="#7a4a25" />
			<circle cx="92" cy="138" r="4" fill="#0c0c0c" />
		</g>
	</svg>

	<div class="text-center">
		<p class="text-base font-medium text-white">세션을 준비하고 있어요</p>
		{#if label}
			<p data-testid="session-loading-splash-label" class="mt-1 text-sm text-[#999]">
				{label}
			</p>
		{/if}
	</div>

	<div class="dots flex gap-1.5" aria-hidden="true">
		<span class="dot"></span>
		<span class="dot"></span>
		<span class="dot"></span>
	</div>
</div>

<style>
	.splash {
		background: radial-gradient(circle at 70% 55%, #161210 0%, #0c0c0c 60%, #000 100%);
	}

	.glow {
		transform-origin: 205px 120px;
		animation: flicker 2.6s ease-in-out infinite;
	}

	.flame {
		transform-origin: 210px 152px;
	}

	.flame-1 {
		animation: flicker 1.4s ease-in-out infinite;
	}

	.flame-2 {
		animation: flicker 1.1s ease-in-out infinite reverse;
	}

	.boy {
		transform-origin: 82px 140px;
		animation: breathe 4s ease-in-out infinite;
	}

	.dot {
		width: 7px;
		height: 7px;
		border-radius: 9999px;
		background: #ff5c16;
		opacity: 0.4;
		animation: pulse 1.2s ease-in-out infinite;
	}

	.dot:nth-child(2) {
		animation-delay: 0.2s;
	}

	.dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes flicker {
		0%,
		100% {
			opacity: 0.9;
			transform: scaleY(1);
		}
		40% {
			opacity: 0.6;
			transform: scaleY(0.92);
		}
		70% {
			opacity: 1;
			transform: scaleY(1.05);
		}
	}

	@keyframes breathe {
		0%,
		100% {
			transform: translateY(0) scale(1);
		}
		50% {
			transform: translateY(-1.5px) scale(1.012);
		}
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 0.3;
			transform: scale(0.85);
		}
		50% {
			opacity: 1;
			transform: scale(1);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.glow,
		.flame,
		.boy,
		.dot {
			animation: none;
		}
	}
</style>
