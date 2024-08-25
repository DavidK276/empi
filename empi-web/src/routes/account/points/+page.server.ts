import * as consts from "$lib/constants";
import type { Participation } from "$lib/objects/participation";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ cookies, fetch, parent }) => {
	const { session } = await parent();

	const formData = new FormData();
	formData.set('password', session?.user_password);
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const response = await fetch(consts.INT_API_ENDPOINT + `participation/user/`, {
			body: formData,
			method: 'POST'
		});
		const responseJSON = await response.json();

		const participations: Participation[] = [];
		for (const participation of responseJSON) {
				participations.push(participation);
		}
		return {participations}
	}
	return {participations: null}
}