import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
	return /^[a-zA-Z0-9-_]{1,32}$/.test(param);
};