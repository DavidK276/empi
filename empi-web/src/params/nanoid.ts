import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
	return /^[A-Z0-9-]{20}$/.test(param);
};