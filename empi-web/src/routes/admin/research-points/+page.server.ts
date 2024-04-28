import type { Actions, PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';
import { paginationParams } from '$lib/functions';

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

export const load: PageServerLoad = async ({ cookies, fetch, url }) => {
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const searchParams = paginationParams(url.searchParams);
		const response = await fetch(consts.API_ENDPOINT + 'research-admin/?' + searchParams);
		if (response.ok) {
			const responseJSON = await response.json();

			return {
				researches: responseJSON.results,
				count: responseJSON.count
			};
		}
	}
	return {};
};