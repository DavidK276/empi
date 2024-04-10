import * as consts from '$lib/constants';
import type { LayoutServerLoad } from './$types';
import { User } from '$lib/objects/user';
import { getUserIdFromUrl } from '$lib/functions';

async function tryGetParticipant(userId: number) {
	const response = await fetch(consts.API_ENDPOINT + `participant/${userId}`, {
		method: 'GET'
	});
	if (response.ok) {
		return await response.json();
	}
	return null;
}


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
		const userId = getUserIdFromUrl(user.url);
		let participant = null;
		if (userId != null) {
			participant = await tryGetParticipant(userId);
		}
		return {
			user: user,
			participant: participant
		};
	}
};