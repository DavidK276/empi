import { defineEnvVars } from "@sveltejs/kit/env";
import * as v from 'valibot';

export const variables = defineEnvVars({
	EMPI_INT_API_ENDPOINT: {
		static: true,
		public: true,
		schema: v.pipe(v.string(), v.url())
	},
	EMPI_EXT_API_ENDPOINT: {
		static: true,
		public: true,
		schema: v.pipe(v.string(), v.url())
	},
	COOKIE_SECRET: {
		description: "Key used to encrypt certain cookies. Must be exactly 32 bytes long.",
		schema: v.pipe(v.string(), v.length(32))
	}
});
