import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import 'dotenv/config';

const ORIGIN = (Object.hasOwn(process.env, 'ORIGIN') ? [process.env.ORIGIN] : []).concat('http://localhost:8000/', 'http://127.0.0.1:8000/');

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(),
		csp: {
			directives: {
				'default-src': ['self'].concat(...ORIGIN),
				'img-src': ['self', 'data:']
			}
		},
		csrf: {
			checkOrigin: true
		}
	}
};

export default config;
