import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { vanillaExtractPlugin } from '@vanilla-extract/vite-plugin';

export default defineConfig(({mode}) => ({
	plugins: [sveltekit(), vanillaExtractPlugin()],
	resolve: {
		conditions: mode === 'test' ? ['browser'] : [],
	},
	test: {
		environment: 'jsdom',
		setupFiles: ['src/lib/tests/setup.ts'],
	}
}));
