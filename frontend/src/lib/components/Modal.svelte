<script lang="ts">
	interface Props {
		open: boolean
		size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl' | '7xl'
		autoclose?: boolean
		class?: string
		children?: import('svelte').Snippet
	}

	let {
		open = $bindable(),
		size = 'xs',
		autoclose = false,
		class: className = '',
		children
	}: Props = $props()

	let modalElement: HTMLDivElement
	let backdropElement: HTMLDivElement

	function handleBackdropClick(event: MouseEvent) {
		if (autoclose && event.target === backdropElement) {
			open = false
		}
	}

	function handleBackdropKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault()
			if (autoclose) {
				open = false
			}
		}
	}

	function handleEscapeKey(event: KeyboardEvent) {
		if (event.key === 'Escape' && open) {
			open = false
		}
	}

	function lockBodyScroll() {
		if (typeof document !== 'undefined') {
			document.body.style.overflow = 'hidden'
		}
	}

	function unlockBodyScroll() {
		if (typeof document !== 'undefined') {
			document.body.style.overflow = ''
		}
	}

	$effect(() => {
		if (open) {
			lockBodyScroll()
			if (typeof window !== 'undefined') {
				window.addEventListener('keydown', handleEscapeKey)
			}
		} else {
			unlockBodyScroll()
			if (typeof window !== 'undefined') {
				window.removeEventListener('keydown', handleEscapeKey)
			}
		}

		return () => {
			unlockBodyScroll()
			if (typeof window !== 'undefined') {
				window.removeEventListener('keydown', handleEscapeKey)
			}
		}
	})

	const sizeClasses = {
		xs: 'max-w-xs',
		sm: 'max-w-sm',
		md: 'max-w-md',
		lg: 'max-w-lg',
		xl: 'max-w-xl',
		'2xl': 'max-w-2xl',
		'3xl': 'max-w-3xl',
		'4xl': 'max-w-4xl',
		'5xl': 'max-w-5xl',
		'6xl': 'max-w-6xl',
		'7xl': 'max-w-7xl'
	}
</script>

{#if open}
	<div
		bind:this={backdropElement}
		class="fixed inset-0 z-40"
		onclick={handleBackdropClick}
		onkeydown={handleBackdropKeydown}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
	>
		<div
			bind:this={modalElement}
			class="modal-dark {sizeClasses[size]} {className}"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.stopPropagation()}
			role="document"
		>
			{#if children}
				{@render children()}
			{/if}
		</div>
	</div>
{/if}

<style>
	:global(.modal-dark) {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: calc(100% - 2rem);
		background: linear-gradient(to right, #1a1410, #0c0c0c) !important;
		border: 1px solid #ff5c16;
		box-shadow: 0px 20px 25px -5px rgba(255, 92, 22, 0.2), 0px 8px 10px -6px rgba(255, 92, 22, 0.2);
		border-radius: 0.75rem;
		z-index: 50;
	}

	:global(.modal-dark > div) {
		background: linear-gradient(to right, #1a1410, #0c0c0c) !important;
		border-radius: 0.75rem;
	}

	:global([data-modal-backdrop]),
	:global(.fixed.inset-0.z-40),
	:global(body > .fixed.inset-0) {
		background-color: rgba(0, 0, 0, 0.85) !important;
		backdrop-filter: blur(2px);
	}
</style>
