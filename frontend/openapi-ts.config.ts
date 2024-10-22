import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
	input: 'https://sessionary-dawn-field-679.fly.dev/openapi.json',
	output: './src/lib/client',
	client: 'axios'
})
