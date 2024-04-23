import type { PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';
import type { User } from '$lib/objects/user';


export const load: PageServerLoad = async ({ fetch, cookies }) => {
	if (cookies.get(consts.TOKEN_COOKIE)) {
		let response = await fetch(consts.API_ENDPOINT + 'user/');

		const users: Map<number, User> = new Map();
		if (response.ok) {
			let responseJSON = await response.json();
			responseJSON.results.forEach((user: User) => {
				users.set(user.id, user);
			});

			while (responseJSON.next != null) {
				response = await fetch(responseJSON.next);

				if (response.ok) {
					responseJSON = await response.json();
					responseJSON.results.forEach((user: User) => {
						users.set(user.id, user);
					});
				}
				else {
					break;
				}
			}
			return {
				users
			};
		}
		else {
			throw error(response.status);
		}
	}
	throw error(401);
};