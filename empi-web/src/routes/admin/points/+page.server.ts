import type { Actions, PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { error, fail } from '@sveltejs/kit';
import type { Research } from '$lib/objects/research';

export const actions = {
	default: async ({ fetch, request }) => {
		const formData = await request.formData();
		const url = formData.get('url');
		if (typeof url == 'string') {
			formData.delete('url');
			const response = await fetch(url, {
				method: 'PATCH',
				body: formData
			});
			if (response.ok) {
				return {
					success: true
				};
			}
			return fail(response.status, { success: false });
		}
		return fail(400, { success: false });
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ cookies, fetch }) => {
	const authToken = cookies.get(consts.TOKEN_COOKIE);
	if (authToken) {
		let response = await fetch(consts.API_ENDPOINT + 'research/', {
			method: 'GET',
			headers: {
				'Authorization': `Token ${authToken}`
			}
		});
		if (response.ok) {
			const researches: Research[] = [];
			let responseJSON = await response.json();

			researches.push(...responseJSON.results);
			while (responseJSON.next != null) {
				response = await fetch(responseJSON.next, {
					method: 'GET',
					headers: {
						'Authorization': `Token ${authToken}`
					}
				});

				if (response.ok) {
					responseJSON = await response.json();
					researches.push(...responseJSON.results);
				}
				else {
					break;
				}
			}

			return {
				researches: researches
			};
		}
	}
	return {};
};