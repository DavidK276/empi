import * as consts from "$lib/constants";
import type { RequestHandler } from "@sveltejs/kit";


export const POST: RequestHandler = async ({cookies}) => {
    const authToken = cookies.get(consts.TOKEN_COOKIE);
    let status = 200;
    if (authToken !== undefined) {
        const response = await fetch(consts.API_ENDPOINT + "auth/logout/", {
            method: 'POST',
            headers: {
                "Authorization": `Token ${authToken}`
            }
        });
        status = response.status;
        cookies.delete(consts.TOKEN_COOKIE, {path: "/"});
    }
    return new Response(null, {status});
}