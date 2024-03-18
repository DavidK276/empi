import { API_ENDPOINT } from "$lib/constants";
import type { PageLoad } from './$types';
import Cookies from 'js-cookie';


export const load: PageLoad = async () => {
    const isLoggedIn = Cookies.get("logged-in") !== undefined;
    console.log("is logged in: " + isLoggedIn);
    if (isLoggedIn) {
        const response = await fetch(API_ENDPOINT + "user/1/", {
            method: 'GET',
            credentials: 'include'
        });
        if (response.status == 403) {
            Cookies.remove("logged-in");
            return;
        }
        const responseJSON = await response.json();
        return {
            first_name: responseJSON.first_name,
            last_name: responseJSON.last_name
        }
    }
};

export const ssr = false;