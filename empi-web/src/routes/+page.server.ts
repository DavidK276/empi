import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';

export const actions = {
	login: async ({ cookies, request }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + 'auth/login/', {
			body: formData,
			method: 'POST'
		});
		cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
		cookies.delete(consts.SELF_URL_COOKIE, { path: '/' });

		if (response.ok) {
			const responseJSON = await response.json();
			const expires = new Date(Date.parse(responseJSON.expiry));
			cookies.set(consts.TOKEN_COOKIE, responseJSON.token, { path: '/', httpOnly: true, expires });
		}
		return {
			login: response.ok
		};
	},
	logout: async ({ cookies }) => {
		const authToken = cookies.get(consts.TOKEN_COOKIE);
		if (authToken !== undefined) {
			await fetch(consts.API_ENDPOINT + 'auth/logout/', {
				method: 'POST',
				headers: {
					'Authorization': `Token ${authToken}`
				}
			});
			cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
		}
	},
	checkPassword: async ({ request, fetch, cookies }) => {
		const authToken = cookies.get(consts.TOKEN_COOKIE);
		let status = 401;
		if (authToken != null) {
			const formData = await request.formData();
			const response = await fetch(consts.API_ENDPOINT + 'user/check_password/', {
				body: formData,
				method: 'POST',
				headers: {
					'Authorization': `Token ${authToken}`
				}
			});
			if (response.ok) {
				return {};
			}
			status = response.status;
		}
		throw error(status);
	}
} satisfies Actions;