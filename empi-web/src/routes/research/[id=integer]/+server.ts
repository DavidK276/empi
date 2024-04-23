import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';

export const POST = async ({ cookies, fetch, request }) => {
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const formData = await request.formData();
		const participationId = formData.get('participation')!;
		formData.delete('participation');
		return await fetch(consts.API_ENDPOINT + `participation/${participationId}/`, {
			body: formData,
			method: 'DELETE'
		});
	}
	throw error(401, 'unauthorized');
}