import * as consts from '$lib/constants';
import { type Actions, error, fail } from '@sveltejs/kit';

export const actions = {
	signup: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		if (cookies.get(consts.TOKEN_COOKIE)) {
			const response = await fetch(consts.API_ENDPOINT + `participation/`, {
				method: 'POST',
				body: formData
			});
			if (response.ok) {
				return {
					success: true,
					participation: null
				};
			}
			return fail(response.status, {
				success: false
			});
		}
		else {
			const response = await fetch(consts.API_ENDPOINT + `anon-participation/`, {
				method: 'POST',
				body: formData
			});
			if (response.ok) {
				return {
					success: true,
					participation: await response.json()
				};
			}
			return fail(response.status, {
				success: false
			});
		}
	},
	cancel: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		const authToken = cookies.get(consts.TOKEN_COOKIE);
		if (authToken != null) {
			const response = await fetch(consts.API_ENDPOINT + `participation/`, {
				method: 'POST',
				body: formData,
				headers: {
					'Authorization': `Token ${authToken}`
				}
			});
			if (response.ok) {
				return {
					success: true
				};
			}
			return fail(response.status, {
				success: false
			});
		}
		throw error(401, 'unuthorized');
	}
} satisfies Actions;