import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';

export const POST = async ({ cookies, fetch, request }) => {
	const authToken = cookies.get(consts.TOKEN_COOKIE);
	if (authToken != null) {
		const formData = await request.formData();
		const participationId = formData.get('participation')!;
		formData.delete('participation');
		return await fetch(consts.API_ENDPOINT + `participation/${participationId}/`, {
			body: formData,
			method: 'DELETE',
			headers: {
				'Authorization': `Token ${authToken}`
			}
		});
	}
	throw error(401, 'unauthorized');
}