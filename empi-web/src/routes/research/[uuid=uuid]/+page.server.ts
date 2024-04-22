import * as consts from '$lib/constants';
import { convertFormData } from '$lib/functions';
import { type Actions, error, fail } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const actions = {
	attrs: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + `attr/research/${params.uuid}/`, {
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
	},
	appointments: async ({ fetch, params, request }) => {
		const response = await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/appointments/`, {
			method: 'PUT',
			body: await request.text(),
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
	},
	participations: async ({ fetch, params, request }) => {
		const response = await fetch(consts.API_ENDPOINT + `participation/research/${params.uuid}/set/`, {
			method: 'POST',
			body: await request.text(),
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
	},
	publish: async ({ fetch, params }) => {
		await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/`, {
			method: 'PATCH',
			body: JSON.stringify({ is_published: true }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	},
	unpublish: async ({ fetch, params }) => {
		await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/`, {
			method: 'PATCH',
			body: JSON.stringify({ is_published: false }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ fetch, params }) => {
	const response = await fetch(consts.API_ENDPOINT + `participation/research/${params.uuid}/get/`, {
		method: 'POST'
	});
	if (response.ok) {
		const responseJSON = await response.json();
		return {
			participations: responseJSON
		};
	}
	throw error(response.status);
};