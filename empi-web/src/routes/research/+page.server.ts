import type { Actions } from './$types';
import * as consts from '$lib/constants';
import { fail, redirect } from '@sveltejs/kit';
import { plainToInstance } from 'class-transformer';
import { Research } from '$lib/objects/research';

export const actions = {
	new: async ({ request }) => {
		const formData = await request.formData();
		const response = await fetch(consts.INT_API_ENDPOINT + 'research-admin/', {
			body: formData,
			method: 'POST'
		});
		const responseJSON = await response.json();
		console.log(responseJSON);
		if (response.ok) {
			const research = plainToInstance(Research, responseJSON);
			// this would ideally be using response.status instead of 302
			// but the method doesn't allow 201 redirects
			throw redirect(302, `research/${research.nanoid}/`);
		}
		return fail(response.status, { success: false, errors: responseJSON });
	}
} satisfies Actions;