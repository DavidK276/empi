import * as consts from '$lib/constants';

export const POST = async ({ fetch, request, params }) => {
	const response = await fetch(consts.API_ENDPOINT + `participation/research/${params.uuid}/get/`, {
		body: await request.formData(),
		method: 'POST'
	});
	return new Response(response.body);
};