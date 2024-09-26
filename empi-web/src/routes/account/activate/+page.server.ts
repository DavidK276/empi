import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';

export const actions = {
	default: async ({ fetch, request, cookies, url }) => {
		const userId = url.searchParams.get('user');
		const resetKey = url.searchParams.get('key');
		if (userId == null || resetKey == null) {
			return fail(401, {success: false, errors: {detail: 'Neplatný odkaz na aktiváciu účtu'}})
		}

		const formData = await request.formData();
		formData.set("passphrase", resetKey);

		if (cookies.get(consts.TOKEN_COOKIE)) {
			const response = await fetch(consts.INT_API_ENDPOINT + `user/${userId}/activate_account/`, {
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