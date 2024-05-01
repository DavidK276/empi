import * as consts from '$lib/constants';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { handleSession } from 'svelte-kit-cookie-session';

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	const urlPath = new URL(request.url).pathname;
	if (request.url.startsWith(consts.DJANGO_SERVER_URL)) {
		const authToken = event.cookies.get(consts.TOKEN_COOKIE);
		const password: string | null = event.locals.session.data.research_password;
		const is_staff = event.locals.user?.is_staff || false;

		if (urlPath.includes('/research-admin') && password && !is_staff) {
			const bytes = new TextEncoder().encode('x:' + password);
			const binString = Array.from(bytes, (byte) =>
				String.fromCodePoint(byte)
			).join('');
			request.headers.set('Authorization', `Basic ${btoa(binString)}`);
		}
		else if (authToken != null) {
			request.headers.set('Authorization', `Token ${authToken}`);
		}
	}

	return fetch(request);
};

const myHandle: Handle = async ({ event, resolve }) => {
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
		const user = event.locals.user;
		if (user != null) {
			if (!user.is_staff) {
				const participantResponse = await event.fetch(consts.API_ENDPOINT + `participant/${user.id}/`);
				if (participantResponse.ok) {
					event.locals.participant = await participantResponse.json();
				}
			}
		}
	}
	return resolve(event);
};

export const handle: Handle = handleSession({
		secret: [
			{
				id: 1,
				secret: '5q~Rp!4QW8d^,K:zB:B1x~CHuyhBp!*M'
			}
		]
	},
	myHandle);