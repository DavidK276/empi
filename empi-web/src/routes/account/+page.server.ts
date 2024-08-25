import type { Actions } from './$types';
import { INT_API_ENDPOINT } from '$lib/constants';
import { fail } from '@sveltejs/kit';

export const actions = {
	updateInfo: async ({ fetch, request, locals }) => {
		const session = locals.session.data;
		const formData = await request.formData();

		const userId = session.user.id;
		if (userId == null) {
			return;
		}
		const response = await fetch(INT_API_ENDPOINT + `user/${userId}/`, {
			method: 'PATCH',
			body: formData
		});
		if (!response.ok) {
			return fail(response.status, { success: false, errors: await response.json() });
		}
		return { success: true }
	},
	changePassword: async ({ fetch, request, locals }) => {
		const session = locals.session.data;
		const formData = await request.formData();

		const userId = session.user.id;
		if (userId == null) {
			return;
		}
		const response = await fetch(INT_API_ENDPOINT + `user/${userId}/change_password/`, {
			method: 'POST',
			body: formData
		});
		if (!response.ok) {
			return fail(response.status, { success: false, errors: await response.json() });
		}
		return { success: true }
	}
} satisfies Actions;