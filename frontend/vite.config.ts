import { sveltekit } from '@sveltejs/kit/vite'
import { alphaTab } from '@coderline/alphatab-vite'
import { defineConfig } from 'vite'

export default defineConfig({
	plugins: [sveltekit(), alphaTab()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		hmr: {
			// compose 경로는 3000:5173 매핑이라 기본 3000. 호스트 devup 은 VITE_HMR_CLIENT_PORT 로 실제 fe 포트를 넘긴다.
			clientPort: Number(process.env.VITE_HMR_CLIENT_PORT) || 3000
		},
		watch: {
			usePolling: true
		}
	}
})
