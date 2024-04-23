import type { Actions, PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';
import type { Research } from '$lib/objects/research';

export const actions = {
	default: async ({ fetch, request, cookies }) => {
		const formData = await request.formData();
		const url = formData.get('url');
		const authToken = cookies.get(consts.TOKEN_COOKIE);

		if (typeof url == 'string' && authToken) {
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
	if (cookies.get(consts.TOKEN_COOKIE)) {
		let response = await fetch(consts.API_ENDPOINT + 'research-admin/');
		if (response.ok) {
			const researches: Research[] = [];
			let responseJSON = await response.json();

			researches.push(...responseJSON.results);
			while (responseJSON.next != null) {
				response = await fetch(responseJSON.next);

				if (response.ok) {
					responseJSON = await response.json();
					researches.push(...responseJSON.results);
				}
				else {
					break;
				}
			}

			return {
				researches
			};
		}
	}
	return {};
};