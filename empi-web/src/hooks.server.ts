import * as consts from '$lib/constants';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { getUserIdFromUrl } from '$lib/functions';

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	if (request.url.startsWith(consts.DJANGO_SERVER_URL)) {
		const authToken = event.cookies.get(consts.TOKEN_COOKIE);
		if (authToken != null) {
			request.headers.set('Authorization', `Token ${authToken}`);
		}
	}

	return fetch(request);
};

export const handle: Handle = async ({ event, resolve }) => {
	const authToken = event.cookies.get(consts.TOKEN_COOKIE);
	if (authToken && event.locals.user == null) {
		const userResponse = await event.fetch(consts.API_ENDPOINT + 'user/get_self/', {
			redirect: 'follow'
		});
		if (!userResponse.ok) {
			event.cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
			return resolve(event);
		}
		event.locals.user = await userResponse.json();

		if (event.locals.user != null) {
			const userId = getUserIdFromUrl(event.locals.user.url);
			if (userId != null && !event.locals.user.is_staff) {
				const participantResponse = await event.fetch(consts.API_ENDPOINT + `participant/${userId}/`);
				if (participantResponse.ok) {
					event.locals.participant = await participantResponse.json();
				}
			}
		}
	}
	return resolve(event);
};