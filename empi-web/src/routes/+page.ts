import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import type { Research } from '$lib/objects/research';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch }) => {
	let response = await fetch(consts.API_ENDPOINT + 'research-user/');

	const researches: Research[] = [];
	if (response.ok) {
		let responseJSON = await response.json();
		researches.push(...responseJSON.results);

		while (responseJSON.next != null) {
			response = await fetch(responseJSON.next);

			if (response.ok) {
				responseJSON = await response.json();
				researches.push(...responseJSON.results);
			}
		}
	}
	else {
		throw error(response.status);
	}
	return {
		researches: researches
	};
};