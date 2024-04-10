import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';
import { convertFormData } from '$lib/functions';


export const actions = {
	default: async ({ cookies, request, fetch }) => {
		const formData = await request.formData();
		const authToken = cookies.get(consts.TOKEN_COOKIE);
		if (authToken) {
			const url = formData.get('url') as string | null;
			const creating = formData.has('create');
			const deleting = formData.has('delete');
			if (deleting && url != null) {
				const response = await fetch(url, {
					method: 'DELETE',
					headers: {
						'Authorization': `Token ${authToken}`
					}
				});
				if (!response.ok) {
					return fail(response.status);
				}
				return {};
			}
			if (creating) {
				formData.delete('create');
				const response = await fetch(consts.API_ENDPOINT + 'attr/', {
					method: 'POST',
					body: convertFormData(formData), // this is needed to support multiple form values with same name
					headers: {
						'Authorization': `Token ${authToken}`,
						'Content-Type': 'application/json'
					}
				});
				if (!response.ok) {
					return fail(response.status);
				}
				return {};
			}
			if (url != null) {
				const response = await fetch(url, {
					method: 'PUT',
					body: convertFormData(formData), // this is needed to support multiple form values with same name
					headers: {
						'Authorization': `Token ${authToken}`,
						'Content-Type': 'application/json'
					}
				});
				if (!response.ok) {
					return fail(response.status);
				}
				return {};
			}
		}
	}
} satisfies Actions;