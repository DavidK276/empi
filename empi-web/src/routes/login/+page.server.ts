import type { Actions } from './$types';
import * as cookie from 'cookie';
import { API_ENDPOINT } from "$lib/constants";

function parseCookie(cookieString: string): {
    name: string,
    value: string,
    opts: Record<string, string> & { path: string }
} {
    const cookieObj = cookie.parse(cookieString);
    for (const name in cookieObj) {
        if (!["max-age", "partitioned", "path", "samesite", "secure", "expires", "domain"].includes(name)) {
            const value = cookieObj[name];
            const path = cookieObj.Path;
            const expires = new Date(Date.parse(cookieObj.expires));
            delete cookieObj[name];
            delete cookieObj.Path;
            delete cookieObj.expires;
            // @ts-expect-error expires has to be a Date for some reason
            return {name, value, opts: {path, expires, ...cookieObj}};
        }
    }
    return {name: "", value: "", opts: {path: ""}};
}

export const actions = {
    default: async ({cookies, request}) => {
        const response = await fetch(API_ENDPOINT + "rest-auth/login/", {
            body: await request.formData(),
            method: 'POST'
        });
        if (response.ok) {
            const setCookies = response.headers.getSetCookie()
            for (const setCookie of setCookies) {
                const cookie = parseCookie(setCookie);
                cookies.set(cookie.name, cookie.value, cookie.opts);
            }
            cookies.set("logged-in", "1", {path: "/", httpOnly: false})
        }
        return {
            success: response.ok
        }
    },
} satisfies Actions;