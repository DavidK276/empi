import * as consts from '$lib/constants';
import type { LayoutServerLoad } from './$types';
import { User } from '$lib/objects/user';


export const load: LayoutServerLoad = async ({ cookies, fetch }) => {
	const authToken = cookies.get(consts.TOKEN_COOKIE);
	if (authToken) {
		const response = await fetch(consts.API_ENDPOINT + 'user/get_self/', {
			method: 'GET',
			redirect: 'follow',
			headers: {
				'Authorization': `Token ${authToken}`
			}
		});
		if (response.status == 401 || response.status == 403) {
			cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
		}
		const user = await response.json() as User;
		return {
			user: user
		};
	}
};