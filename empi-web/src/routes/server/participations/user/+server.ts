import * as consts from "$lib/constants";
import { error } from "@sveltejs/kit";

export const POST = async ({ cookies, fetch, request }) => {
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const response = await fetch(consts.API_ENDPOINT + `participation/user/`, {
			body: await request.formData(),
			method: 'POST'
		});
		return new Response(response.body);
	}
	throw error(401, 'unauthorized');
}