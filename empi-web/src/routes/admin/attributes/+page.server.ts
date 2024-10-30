import type { Actions, PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { fail } from '@sveltejs/kit';
import { convertFormData } from '$lib/functions';


export const actions = {
	admin: async ({ cookies, request, fetch }) => {
		const formData = await request.formData();
		if (cookies.get(consts.TOKEN_COOKIE)) {
			const url = formData.get('url') as string | null;
			const creating = formData.has('create');
			const deleting = formData.has('delete');
			if (deleting && url != null) {
				const response = await fetch(url, {
					method: 'DELETE'
				});
				if (!response.ok) {
					return fail(response.status);
				}
				return {};
			}
			if (creating) {
				formData.delete('create');
				const response = await fetch(consts.INT_API_ENDPOINT + 'attr/', {
					method: 'POST',
					body: convertFormData({ formData }), // this is needed to support multiple form values with same name
					headers: {
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
					body: convertFormData({ formData }), // this is needed to support multiple form values with same name
					headers: {
						'Content-Type': 'application/json'
					}
				});
				if (!response.ok) {
					return fail(response.status);
				}
				return {};
			}
		}
	},
	user: async ({ cookies, request, fetch, locals }) => {
		const session = locals.session.data;
		const formData = await request.formData();

		if (cookies.get(consts.TOKEN_COOKIE) && !session.user.is_staff) {
			const response = await fetch(consts.INT_API_ENDPOINT + `attr/participant/${session.user.id}/`, {
				method: 'POST',
				body: convertFormData({ formData }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			if (response.ok) {
				return {
					success: true
				};
			}
			return fail(response.status, {
				success: false
			});
		}
		return fail(401, {
			success: false
		});
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ cookies, fetch, parent }) => {
	const { session } = await parent();

	if (cookies.get(consts.TOKEN_COOKIE) && session?.user.is_staff === false) {
		const response = await fetch(consts.INT_API_ENDPOINT + `attr/participant/${session.user.id}/`);
		if (response.ok) {
			const responseJSON = await response.json();
			return {
				user_attrs: responseJSON
			};
		}
	}
	return {};
};