import * as consts from '$lib/constants';
import { columnify, convertFormData } from '$lib/functions';
import { type Actions, fail } from '@sveltejs/kit';
import { Attribute } from '$lib/objects/attribute';
import type { Appointment } from '$lib/objects/appointment';
import type { PageServerLoad } from './$types';
import type { Participation } from '$lib/objects/participation';

export const actions = {
	update: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/`, {
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
		const response = await fetch(consts.INT_API_ENDPOINT + `attr/research/${params.nanoid}/`, {
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
		const response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/appointments/`, {
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
			success: false,
			errors: await response.json()
		});
	},
	participations: async ({ fetch, params, request }) => {
		const response = await fetch(consts.INT_API_ENDPOINT + `participation/research/${params.nanoid}/set/`, {
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
	publish: async ({ fetch, params }) => {
		await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/`, {
			method: 'PATCH',
			body: JSON.stringify({ is_published: true }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	},
	unpublish: async ({ fetch, params }) => {
		await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/`, {
			method: 'PATCH',
			body: JSON.stringify({ is_published: false }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	},
	setPassword: async ({ fetch, params, request, locals }) => {
		const formData = await request.formData();
		const response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/password/set/`, {
			method: 'POST',
			body: formData
		});
		if (response.ok) {
			await locals.session.update(() => ({ research_password: formData.get('new_password') }));
			return {
				success: true
			};
		}
		return fail(response.status, {
			success: false,
			errors: await response.json()
		});
	},
	checkPassword: async ({ fetch, params, request, locals }) => {
		let formData = await request.formData();
		const session = locals.session.data;

		let password = formData.get('password');
		if (password == null) {
			password = session.research_password || 'unprotected';
			formData = new FormData();
			formData.set('password', password!);
		}
		const response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/password/check/`, {
			body: formData,
			method: 'POST'
		});
		if (response.ok) {
			await locals.session.update(() => ({ research_password: password }));
			return {success: true};
		}
		await locals.session.update(() => ({ research_password: undefined }));
		return fail(response.status, {success: false, errors: await response.json()});
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ params, fetch, locals }) => {
	let research = null;
	let response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/`);
	if (response.ok) {
		research = await response.json();
	}

	let research_attrs = null;
	response = await fetch(consts.INT_API_ENDPOINT + `attr/research/${params.nanoid}/`);
	if (response.ok) {
		research_attrs = await response.json();
	}

	const attrs: Attribute[] = [];
	response = await fetch(consts.INT_API_ENDPOINT + 'attr/');
	if (response.ok) {
		let responseJSON = await response.json();
		attrs.push(...responseJSON.results);

		while (responseJSON.next != null) {
			response = await fetch(responseJSON.next);

			if (response.ok) {
				responseJSON = await response.json();
				attrs.push(...responseJSON.results);
			}
		}
	}

	let appointments: Appointment[] = [];
	response = await fetch(consts.INT_API_ENDPOINT + `research-admin/${params.nanoid}/appointments/`);
	if (response.ok) {
		appointments = await response.json();
	}

	let participations: Participation[][] = [];
	const password = locals.session.data.research_password;
	if (password != null) {
		const formData = new FormData();
		formData.set('password', password);
		response = await fetch(consts.INT_API_ENDPOINT + `participation/research/${params.nanoid}/get/`, {
			body: formData,
			method: 'POST'
		});
		if (response.ok) {
			participations = columnify(await response.json(), 3) as Participation[][];
		}
	}
	return {
		research,
		attrs,
		research_attrs,
		appointments,
		participations
	};
};