import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import type { Research } from '$lib/objects/research';
import { error } from '@sveltejs/kit';
import type { Appointment } from '$lib/objects/appointment';

export const load: PageLoad = async ({ fetch, params }) => {
	let response = await fetch(consts.API_ENDPOINT + `research-user/${params.id}/`);

	let research: Research | null = null;
	if (response.ok) {
		research = await response.json();
	}
	else {
		throw error(response.status);
	}

	response = await fetch(consts.API_ENDPOINT + `research-user/${params.id}/appointments/`);
	const appointments: Appointment[] = [];
	if (response.ok) {
		let responseJSON = await response.json();
		appointments.push(...responseJSON);

		while (responseJSON.next != null) {
			response = await fetch(responseJSON.next);

			if (response.ok) {
				responseJSON = await response.json();
				appointments.push(...responseJSON.results);
			}
		}
	}
	else {
		throw error(response.status);
	}

	return {
		research,
		appointments
	};
};