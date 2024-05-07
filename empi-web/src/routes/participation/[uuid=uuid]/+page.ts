import type { PageLoad } from "./$types";
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';
import { Appointment } from '$lib/objects/appointment';
import { plainToInstance } from 'class-transformer';
import { browser } from "$app/environment";

const API_ENDPOINT = (browser) ? consts.EXT_API_ENDPOINT : consts.INT_API_ENDPOINT;


export const load: PageLoad = async ({fetch, params}) => {
	let response = await fetch(API_ENDPOINT + `anon-participation/${params.uuid}/`);
	if (response.ok) {
		let responseJSON = await response.json();
		const appointment = plainToInstance(Appointment, responseJSON.appointment_detail);

		response = await fetch(API_ENDPOINT + `research-user/${appointment.research}/`)
		responseJSON = await response.json();

		return {
			appointment,
			research: responseJSON
		}
	}
	throw error(response.status);
};