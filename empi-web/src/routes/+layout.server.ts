import * as consts from "$lib/constants";
import type { LayoutServerLoad } from './$types';


export const load: LayoutServerLoad = async ({cookies, fetch}) => {
    const authToken = cookies.get(consts.TOKEN_COOKIE);
    if (authToken !== undefined) {
        const response = await fetch(consts.API_ENDPOINT + "user/1/", {
            method: 'GET',
            headers: {
                "Authorization": `Token ${authToken}`
            }
        });
        if (response.status == 403) {
            cookies.delete(consts.TOKEN_COOKIE, {path: "/"});
        }
        return {
            user: await response.json(),
        };
    }
};