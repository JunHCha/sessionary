<script lang="ts">
	import { Button } from 'flowbite-svelte'
</script>

<section class="flex flex-col items-center justify-center h-screen bg-surface-default">
	<h1 class="text-9xl font-extrabold text-brand-primary">404</h1>
	<p class="mt-4 text-3xl tracking-tight font-bold text-white md:text-4xl">
		Something's missing.
	</p>
	<p class="mt-4 text-lg font-light text-content-muted">
		Sorry, we can't find that page. You'll find lots to explore on the home page.
	</p>
	<Button href="/home" size="lg" class="mt-8">Back to Homepage</Button>
</section>
