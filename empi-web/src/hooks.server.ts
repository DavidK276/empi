import * as consts from "$lib/constants";
import type { HandleFetch } from "@sveltejs/kit";

export const handleFetch: HandleFetch = async ({event, request, fetch}) => {
    if (request.url.startsWith(consts.DJANGO_SERVER_URL)) {
        const cookieHeader = event.request.headers.get('cookie');
        if (cookieHeader !== null) {
            request.headers.set('cookie', cookieHeader);
        }
    }

    return fetch(request);
};