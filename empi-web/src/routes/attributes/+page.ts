import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import { Attribute } from '$lib/objects/attribute';
import { browser } from '$app/environment';

const API_ENDPOINT = (browser) ? consts.EXT_API_ENDPOINT : consts.INT_API_ENDPOINT;


export const load: PageLoad = async ({ fetch, parent, data }) => {
	let response = await fetch(API_ENDPOINT + 'attr/');

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
	await parent();
	return {
		attrs: attrs,
		user_attrs: data.user_attrs
	};
};