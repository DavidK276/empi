import type { Actions } from './$types';
import * as consts from "$lib/constants";

export const actions = {
    login: async ({cookies, request}) => {
        const formData = await request.formData();
        const response = await fetch(consts.API_ENDPOINT + "auth/login/", {
            body: formData,
            method: 'POST',
        });
        cookies.delete(consts.TOKEN_COOKIE, {path: "/"});

        if (response.ok) {
            const responseJSON = await response.json();
            const expires = new Date(Date.parse(responseJSON.expiry));
            cookies.set(consts.TOKEN_COOKIE, responseJSON.token, {path: "/", httpOnly: true, expires});
        }
    },
    logout: async ({cookies}) => {
        const authToken = cookies.get(consts.TOKEN_COOKIE);
        if (authToken !== undefined) {
            await fetch(consts.API_ENDPOINT + "auth/logout/", {
                method: 'POST',
                headers: {
                    "Authorization": `Token ${authToken}`
                }
            });
            cookies.delete(consts.TOKEN_COOKIE, {path: "/"});
        }
    }
} satisfies Actions;