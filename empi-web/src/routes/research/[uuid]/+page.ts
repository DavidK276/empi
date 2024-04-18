import type { PageLoad } from './$types';
import { API_ENDPOINT } from '$lib/constants';
import { error } from '@sveltejs/kit';
import { Attribute } from '$lib/objects/attribute';
import type { Appointment } from '$lib/objects/appointment';

export const load: PageLoad = async ({ params, fetch }) => {
	let research = null;
	let response = await fetch(API_ENDPOINT + `research/${params.uuid}/`);
	if (response.ok) {
		research = await response.json();
	}
	else {
		return error(response.status);
	}

	let research_attrs = null;
	response = await fetch(API_ENDPOINT + `attr/research/${params.uuid}/`);
	if (response.ok) {
		research_attrs = await response.json();
	}
	else {
		error(response.status);
	}

	const attrs: Attribute[] = [];
	response = await fetch(API_ENDPOINT + 'attr/');
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
	else {
		error(response.status);
	}

	let appointments: Appointment[] = [];
	response = await fetch(API_ENDPOINT + `research/${params.uuid}/appointments/`);
	if (response.ok) {
		appointments = await response.json();
	}
	else {
		error(response.status);
	}

	return {
		research,
		attrs,
		research_attrs,
		appointments
	};
};