import { type Actions, fail, redirect } from '@sveltejs/kit';
import * as consts from '$lib/constants';

export const actions = {
	cancel: async ({fetch, params}) => {
		const response = await fetch(consts.INT_API_ENDPOINT + `anon-participation/${params.nanoid}/`, {
			method: 'DELETE'
		});
		if (response.ok) {
			throw redirect(302, 'cancel-ok');
		}
		return fail(response.status, {success: false});
	}
} satisfies Actions;