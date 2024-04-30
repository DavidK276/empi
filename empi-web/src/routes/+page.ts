import type { PageLoad } from './$types';
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';
import { paginationParams } from '$lib/functions';

export const load: PageLoad = async ({ fetch, url }) => {
	const searchParams = paginationParams(url.searchParams);
	const response = await fetch(consts.API_ENDPOINT + 'research-user/?' + searchParams.toString());

	if (response.ok) {
		const responseJSON = await response.json();
		return {
			researches: responseJSON.results,
			count: responseJSON.count
		};
	}
	throw error(response.status);
};