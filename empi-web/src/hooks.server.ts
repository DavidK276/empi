import * as consts from '$lib/constants';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { handleSession } from 'svelte-kit-cookie-session';

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	const urlPath = new URL(request.url).pathname;
	if (request.url.startsWith(consts.INT_SERVER_URL)) {
		const authToken = event.cookies.get(consts.TOKEN_COOKIE);

		const session = event.locals.session.data;
		const password: string | null = session.research_password;
		const is_staff = session.user?.is_staff || false;

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
	if (!event.cookies.get(consts.TOKEN_COOKIE)) {
		await event.locals.session.update(() => ({user: undefined, user_password: undefined, participant: undefined}));
		return resolve(event);
	}
	if (!event.locals.session.data.user) {
		const userResponse = await event.fetch(consts.INT_API_ENDPOINT + 'user/get_self/', {
			redirect: 'follow'
		});
		if (!userResponse.ok) {
			event.cookies.delete(consts.TOKEN_COOKIE, { path: '/' });
		await event.locals.session.update(() => ({user: undefined, user_password: undefined, participant: undefined}));
			return resolve(event);
		}

		const user = await userResponse.json();
		await event.locals.session.update(async () => ({ user }));
	}

	if (!event.locals.session.data.participant) {
		const user = event.locals.session.data.user;
		if (!user.is_staff) {
			const participantResponse = await event.fetch(consts.INT_API_ENDPOINT + `participant/${user.id}/`);
			if (!participantResponse.ok) {
				await event.locals.session.update(() => ({ participant: undefined }));
				return resolve(event);
			}

			const participant = await participantResponse.json();
			await event.locals.session.update(async () => ({ participant }));
		}
	}

	return resolve(event);
};

export const handle: Handle = handleSession({
			secret: [
				{
					id: 1,
					secret: process.env.COOKIE_SECRET || 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
				}
			]
		},
		myHandle);