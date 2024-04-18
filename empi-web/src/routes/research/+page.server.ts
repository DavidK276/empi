import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	new: async ({ request }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + 'research-admin/', {
			body: formData,
			method: 'POST'
		});
		const location = response.headers.get('Location');
		if (location != null) {
			const url = new URL(location);
			const pathParts = url.pathname.split('/');
			if (pathParts[pathParts.length - 1] === '') {
				pathParts.pop();
			}
			const researchUUID = pathParts[pathParts.length - 1];
			// this should be using response.status instead of 302, but the method doesn't allow 201 redirects
			throw redirect(302, `research/${researchUUID}/`)
		}
		return fail(response.status, { success: false });
	}
} satisfies Actions;