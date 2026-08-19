import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import Icons from 'unplugin-icons/vite';
import { sentrySvelteKit } from '@sentry/sveltekit';

export default defineConfig(() => ({
	plugins: [
		sentrySvelteKit({
			org: 'znama-firma-sro',
			project: 'empi-web',
			sentryUrl: 'https://glitchtip.znamafirma.xyz/',
			
		}),
		sveltekit(),
		Icons({
			compiler: 'svelte'
		})
	]
}));
