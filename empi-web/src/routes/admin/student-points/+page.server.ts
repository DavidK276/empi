import type { PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { error } from '@sveltejs/kit';
import type { User } from '$lib/objects/user';


export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const authToken = cookies.get(consts.TOKEN_COOKIE);
	if (authToken != null) {
		let response = await fetch(consts.API_ENDPOINT + 'user/', {
			headers: {
				'Authorization': `Token ${authToken}`
			}
		});

		const users: Map<string, User> = new Map();
		if (response.ok) {
			let responseJSON = await response.json();
			responseJSON.results.forEach((user: User) => {
				users.set(user.url, user);
			});

			while (responseJSON.next != null) {
				response = await fetch(responseJSON.next);

				if (response.ok) {
					responseJSON = await response.json();
					responseJSON.results.forEach((user: User) => {
						users.set(user.url, user);
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