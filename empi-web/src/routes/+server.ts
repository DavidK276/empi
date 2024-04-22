import * as consts from "$lib/constants";
import { error } from "@sveltejs/kit";

export const POST = async ({ cookies, fetch, request }) => {
	const authToken = cookies.get(consts.TOKEN_COOKIE);
	if (authToken != null) {
		const response = await fetch(consts.API_ENDPOINT + `participation/user/`, {
			body: await request.formData(),
			method: 'POST',
			headers: {
				'Authorization': `Token ${authToken}`
			}
		});
		return new Response(response.body);
	}
	throw error(401, 'unauthorized');
}