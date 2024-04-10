import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import { Attribute } from '$lib/objects/attribute';

export const load: PageLoad = async ({ fetch }) => {
	let response = await fetch(consts.API_ENDPOINT + 'attr/');

	const attrs: Attribute[] = [];
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
	return {
		attrs: attrs
	};
};