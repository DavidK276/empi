import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { error, fail } from '@sveltejs/kit';
import { resolve } from "$app/paths";

export const actions = {
	login: async ({ cookies, request, locals, fetch }) => {
		const formData = await request.formData();
		const response = await fetch(consts.INT_API_ENDPOINT + 'auth/login/', {
			body: formData,
			method: 'POST'
		});

		await locals.session.destroy();
		cookies.delete(consts.TOKEN_COOKIE, { path: resolve('/') });

		const responseJSON = await response.json();
		if (response.ok) {
			const expires = new Date(Date.parse(responseJSON.expiry));
			cookies.set(consts.TOKEN_COOKIE, responseJSON.token, { path: resolve('/'), httpOnly: true, expires });
			await locals.session.update(() => ({ user_password: formData.get('password') }));
			return { login: true };
		}
		if (response.status === 401) {
			return fail(401, { login: false, errors: responseJSON });
		}
		throw error(response.status);
	},
	logout: async ({ cookies, locals, fetch }) => {
		if (cookies.get(consts.TOKEN_COOKIE)) {
			await fetch(consts.INT_API_ENDPOINT + 'auth/logout/', {
				method: 'POST'
			});

			await locals.session.destroy();
			cookies.delete(consts.TOKEN_COOKIE, { path: resolve('/') });
		}
	},
	checkPassword: async ({ request, fetch, cookies, locals }) => {
		if (cookies.get(consts.TOKEN_COOKIE)) {
			const formData = await request.formData();
			const password = formData.get('password');

			const response = await fetch(consts.INT_API_ENDPOINT + 'user/check_password/', {
				body: formData,
				method: 'POST'
			});
			if (response.ok) {
				await locals.session.update(() => ({ user_password: password }));
				return {};
			}
			throw error(response.status);
		}
		throw error(401);
	}
} satisfies Actions;
