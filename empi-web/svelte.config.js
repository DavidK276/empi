import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const origin = (Object.hasOwn(process.env, 'ORIGIN') ? [process.env.ORIGIN] : []);

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
				'default-src': ['self'].concat(...origin).concat('http://localhost:8000/', 'http://127.0.0.1:8000/'),
				'img-src': ['self', 'data:'],
				'style-src-attr': ['unsafe-inline']
			}
		},
		csrf: {
			checkOrigin: true
		},
		env: {
			publicPrefix: "EMPI_"
		}
	}
};

export default config;
