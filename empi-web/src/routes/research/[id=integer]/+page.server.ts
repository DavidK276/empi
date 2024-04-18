import type { Actions } from './$types';

export const actions = {
	test: () => {
		return {
			clicked: true
		}
	}
} satisfies Actions;