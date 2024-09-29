import * as consts from '$lib/constants';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { handleSession } from 'svelte-kit-cookie-session';
import { base } from "$app/paths";
import * as env from '$env/static/private';

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	const urlPath = new URL(request.url).pathname;
	if (request.url.startsWith(consts.INT_API_ENDPOINT)) {
		const authToken = event.cookies.get(consts.TOKEN_COOKIE);

		const session = event.locals.session.data;
		const nanoid: string | null = session.research_nanoid;
		const password: string | null = session.research_password;

		if ((urlPath.includes(`${base}/research-admin`) || urlPath.includes(`${base}/email/send_research_info`)) && nanoid && password) {
			request.headers.set('Authorization', `Basic ${btoa(`${nanoid}:${password}`)}`);
		}
		else if (authToken != null) {
			request.headers.set('Authorization', `Bearer ${authToken}`);
		}
	}

	return fetch(request);
};

const myHandle: Handle = async ({ event, resolve }) => {
	if (!event.cookies.get(consts.TOKEN_COOKIE)) {
		await event.locals.session.update(() => ({ user: undefined, user_password: undefined, participant: undefined }));
		return resolve(event);
	}
	if (!event.locals.session.data.user) {
		const userResponse = await event.fetch(consts.INT_API_ENDPOINT + 'user/get_self/', {
			redirect: 'follow'
		});
		if (!userResponse.ok) {
			event.cookies.delete(consts.TOKEN_COOKIE, { path: base });
			await event.locals.session.update(() => ({ user: undefined, user_password: undefined, participant: undefined }));
			return resolve(event);
		}

		const user = await userResponse.json();
		await event.locals.session.update(async () => ({ user }));
	}

	if (!event.locals.session.data.participant) {
		const user = event.locals.session.data.user;
		if (user.token != null) {
			const participantResponse = await event.fetch(consts.INT_API_ENDPOINT + `participant/${user.token}/`);
			if (!participantResponse.ok) {
				await event.locals.session.update(() => ({ participant: undefined }));
				return resolve(event);
			}

			const participant = await participantResponse.json();
			await event.locals.session.update(async () => ({ participant }));
		}
		else {
			await event.locals.session.update(async () => ({ participant: undefined }));
		}
	}

	return resolve(event);
};

export const handle: Handle = handleSession({
			secret: [
				{
					id: 1,
					secret: env.COOKIE_SECRET || 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
				}
			]
		},
		myHandle);