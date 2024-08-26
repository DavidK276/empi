import type { PageServerLoad } from './$types';
import * as consts from '$lib/constants';


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
		const participations: Map<string, {name: string, points: number}> = new Map();
		const researches: Map<number, number> = new Map<number, number>();
		for (const participation of responseJSON) {
			const token = participation.token;
			const researchId = participation.research;

			const participantResponse = await fetch(consts.INT_API_ENDPOINT + `participant/${token}/`);
			const participantDetail = await participantResponse.json();
			const name = participantDetail.user_detail.first_name + ' ' + participantDetail.user_detail.last_name;

			if (!researches.has(researchId)) {
				const researchResponse = await fetch(consts.INT_API_ENDPOINT + `research-user/${researchId}/`);
				const researchDetail = await researchResponse.json();
				researches.set(researchId, researchDetail.points);
			}

			const currentPoints = participations.get(token)?.points || 0;
			participations.set(token, {name, points: researches.get(researchId)! + currentPoints})
		}
		return {participations}
	}
	return {participations: null}
}