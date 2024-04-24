import { type Actions, fail } from '@sveltejs/kit';
import * as consts from '$lib/constants';

export const actions = {
	cancel: async ({fetch, params}) => {
		const response = await fetch(consts.API_ENDPOINT + `anon-participation/${params.uuid}/`, {
			method: 'DELETE'
		});
		if (response.ok) {
			return {
				success: true
			}
		}
		return fail(response.status, {success: false});
	}
} satisfies Actions;