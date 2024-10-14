import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import type { Research } from '$lib/objects/research';
import { error } from '@sveltejs/kit';
import type { Appointment } from '$lib/objects/appointment';
import { browser } from '$app/environment';

const API_ENDPOINT = (browser) ? consts.EXT_API_ENDPOINT : consts.INT_API_ENDPOINT;

export const load: PageLoad = async ({ fetch, params, data }) => {
	// eslint-disable-next-line prefer-const
	let { participations, canSignup } = data;
	let response = await fetch(API_ENDPOINT + `research-user/${params.id}/`);

	let research: Research | null = null;
	if (response.ok) {
		research = await response.json();
	}
	else {
		throw error(response.status);
	}

	response = await fetch(API_ENDPOINT + `research-user/${params.id}/appointments/`);
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

	let isConfirmed = false;

	for (const participation of data.participations?.values() || []) {
		if (participation.research.id === research?.id) {
			canSignup = false;
			isConfirmed ||= participation.is_confirmed;
			break;
		}
	}

	return {
		research,
		appointments,
		participations,
		canSignup,
		isConfirmed
	};
};