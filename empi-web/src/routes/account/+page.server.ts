import type { Actions } from './$types';
import { INT_API_ENDPOINT } from '$lib/constants';
import { fail } from '@sveltejs/kit';

export const actions = {
	default: async ({ fetch, request, locals }) => {
		const formData = await request.formData();
		const userId = locals.user?.id;
		if (userId == null) {
			return;
		}
		const response = await fetch(INT_API_ENDPOINT + `user/${userId}/`, {
			method: 'PATCH',
			body: formData
		});
		if (!response.ok) {
			return fail(response.status);
		}
	}
} satisfies Actions;