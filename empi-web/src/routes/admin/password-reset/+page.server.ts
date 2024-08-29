import type { Actions, PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';

export const actions = {
	default: async ({ fetch, request, cookies, locals }) => {
		const formData = await request.formData();

		if (cookies.get(consts.TOKEN_COOKIE)) {
			formData.set("password", locals.session?.data.user_password);
			const response = await fetch(consts.INT_API_ENDPOINT + 'user/start_password_reset/', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				return fail(response.status, { success: false, errors: await response.json() });
			}
			return { success: true };
		}
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ fetch }) => {

};