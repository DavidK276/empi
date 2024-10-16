import type { PageServerLoad } from './$types';
import * as consts from '$lib/constants';


export const load: PageServerLoad = async ({ cookies, fetch, locals, request }) => {
	const formData = new FormData();
	formData.set('password', locals.session.data.user_password);

	const searchParams = new URL(request.url).searchParams;
	const currentDate = new Date();

	const year = searchParams.get('year') || currentDate.getFullYear().toString();
	const semester = searchParams.get('semester') || (currentDate.getMonth() >= 7 ? 'z' : 'l');

	if (cookies.get(consts.TOKEN_COOKIE)) {
		const response = await fetch(consts.INT_API_ENDPOINT + `participation/user/?year=${year}`, {
			body: formData,
			method: 'POST'
		});
		const responseJSON = await response.json();
		const participationMap: Map<string, {
			name: string,
			unconfirmedPoints: number,
			confirmedPoints: number
		}> = new Map();
		for (const participation of responseJSON) {
			if (participation.participant.year == year && participation.participant.semester == semester) {
				const token = participation.participant.token;
				const name = participation.participant.user_detail.first_name + ' ' + participation.participant.user_detail.last_name;
				const currentParticipation = participationMap.get(token) || { name, unconfirmedPoints: 0, confirmedPoints: 0 };
				if (participation.is_confirmed) {
					participationMap.set(token, {
						name,
						unconfirmedPoints: currentParticipation.unconfirmedPoints,
						confirmedPoints: currentParticipation.confirmedPoints + participation.research.points
					});
				}
				else {
					participationMap.set(token, {
						name,
						unconfirmedPoints: currentParticipation.unconfirmedPoints + participation.research.points,
						confirmedPoints: currentParticipation.confirmedPoints
					});
				}

			}
		}
		return { participations: Array.from(participationMap.values()) };
	}
	return { participations: null };
};