import type { Actions } from './$types';
import * as consts from '$lib/constants';

export const actions = {
	new: async ({ request }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + 'research/', {
			body: formData,
			method: 'POST'
		});
		if (response.ok) {
			const responseJSON = await response.json();
			return {
				success: response.ok,
				research: responseJSON
			}
		}
	}
} satisfies Actions;