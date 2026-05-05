import { sveltekit } from '@sveltejs/kit/vite'
import { alphaTab } from '@coderline/alphatab-vite'
import { defineConfig } from 'vite'

export default defineConfig({
	plugins: [sveltekit(), alphaTab()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		hmr: {
			clientPort: 3000
		},
		watch: {
			usePolling: true
		}
	}
})
