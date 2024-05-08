import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';

export const DELETE = async ({ cookies, fetch, request, params }) => {
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const formData = await request.formData();
		return await fetch(consts.INT_API_ENDPOINT + `participation/${params.id}/`, {
			body: formData,
			method: 'DELETE'
		});
	}
	throw error(401, 'unauthorized');
}