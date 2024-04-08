import type { Actions } from '@sveltejs/kit';
import { fail } from '@sveltejs/kit';
import * as consts from '$lib/constants';

export const actions = {
	default: async ({ request }) => {
		const response = await fetch(consts.API_ENDPOINT + 'participant/register/', {
			method: 'POST',
			body: await request.formData()
		});
		const responseJSON = await response.json();
		if (!response.ok) {
			return fail(response.status, { failure: true, body: responseJSON });
		}
		return {
			success: true,
			body: responseJSON
		};
	}
} satisfies Actions;