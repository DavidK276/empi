import * as consts from '$lib/constants';
import { type Actions, error, fail, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { IParticipation } from '$lib/objects/participation';

export const actions = {
	signup: async ({ request, fetch, cookies, locals }) => {
		const session = locals.session.data;
		const formData = await request.formData();

		if (cookies.get(consts.TOKEN_COOKIE)) {
			formData.set('password', session.user_password);
			const response = await fetch(consts.INT_API_ENDPOINT + `participation/signup/`, {
				method: 'POST',
				body: formData
			});
			if (response.ok) {
				return {
					success: true,
				};
			}
			return fail(response.status, {
				success: false
			});
		}
		const response = await fetch(consts.INT_API_ENDPOINT + `anon-participation/`, {
			method: 'POST',
			body: formData
		});
		const participation = await response.json();
		if (response.ok) {
			return redirect(302, `/participation/${participation.nanoid}`);
		}
		return fail(response.status, {
			success: false
		});
	},
	cancel: async ({ request, fetch, cookies, locals }) => {
		const session = locals.session.data;
		const formData = await request.formData();
		const participationId = formData.get('participation-id');

		const authToken = cookies.get(consts.TOKEN_COOKIE);
		if (authToken != null) {
			const response = await fetch(consts.INT_API_ENDPOINT + `participation/${participationId}/?password=${session.user_password}`, {
				method: 'DELETE'
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
		throw error(401, 'unuthorized');
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ cookies, fetch, parent }) => {
	const { session } = await parent();
	if (session?.user?.is_staff) {
		return { participations: null, canSignup: false };
	}
	if (!cookies.get(consts.TOKEN_COOKIE)) {
		return { participations: null, canSignup: true };
	}

	const formData = new FormData();
	formData.set('password', session?.user_password);
	const participations = fetch(consts.INT_API_ENDPOINT + `participation/user/`, {
		body: formData,
		method: 'POST'
	}).then(async (response) => {
		if (!response.ok) {
			throw error(response.status);
		}
		const responseJSON = await response.json();
		const participations: Map<number, IParticipation> = new Map();
		for (const participation of responseJSON) {
			participations.set(participation.appointment, participation);
		}
		return participations;
	});

	return { participations, canSignup: true };
};