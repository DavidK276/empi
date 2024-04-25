import * as consts from '$lib/constants';
import { convertFormData } from '$lib/functions';
import { type Actions, error, fail } from '@sveltejs/kit';

export const actions = {
	update: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/`, {
			method: 'PATCH',
			body: formData
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
	},
	setPassword: async ({fetch, params, request}) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/password/set/`, {
			method: 'POST',
			body: formData
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
	checkPassword: async ({fetch, params, request}) => {
		const formData = await request.formData();
		const response = await fetch(consts.API_ENDPOINT + `research-admin/${params.uuid}/password/check/`, {
			body: formData,
			method: 'POST'
		});
		if (response.ok) {
			return {};
		}
		throw error(response.status);
	}
} satisfies Actions;