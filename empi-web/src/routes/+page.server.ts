import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';

export const actions = {
	login: async ({ cookies, request, locals, fetch }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + 'auth/login/', {
			body: formData,
			method: 'POST'
		});
		cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
		delete locals.user;
		delete locals.participant;

		if (response.ok) {
			const responseJSON = await response.json();
			const expires = new Date(Date.parse(responseJSON.expiry));
			cookies.set(consts.TOKEN_COOKIE, responseJSON.token, { path: '/', httpOnly: true, expires });
		}
		return {
			login: response.ok
		};
	},
	logout: async ({ cookies, locals, fetch }) => {
		if (cookies.get(consts.TOKEN_COOKIE)) {
			await fetch(consts.API_ENDPOINT + 'auth/logout/', {
				method: 'POST'
			});
			cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
			delete locals.user;
			delete locals.participant;
		}
	},
	checkPassword: async ({ request, fetch, cookies }) => {
		let status = 401;
		if (cookies.get(consts.TOKEN_COOKIE)) {
			const formData = await request.formData();
			const response = await fetch(consts.API_ENDPOINT + 'user/check_password/', {
				body: formData,
				method: 'POST'
			});
			if (response.ok) {
				return {};
			}
			status = response.status;
		}
		throw error(status);
	}
} satisfies Actions;