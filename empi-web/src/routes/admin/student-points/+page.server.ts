import type { PageServerLoad } from './$types';
import * as consts from '$lib/constants';
import { getCurrentAcademicYear, getCurrentSemester } from "$lib/settings";

async function getParticipations(fetch: Function, formData: FormData, year: string, semester: string) {
	const response = await fetch(consts.INT_API_ENDPOINT + `participation/user/?year=${year}&semester=${semester}`, {
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
	const participations = Array.from(participationMap.values());
	participations.sort((a, b) => {
		const textA = a.name.toUpperCase().split(' ', 2)[1];
		const textB = b.name.toUpperCase().split(' ', 2)[1];
		return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
	})
	return participations;
}

export const load: PageServerLoad = async ({ cookies, fetch, locals, request }) => {
	const formData = new FormData();
	formData.set('password', locals.session.data.user_password);

	const searchParams = new URL(request.url).searchParams;

	const year = searchParams.get('year') || getCurrentAcademicYear(locals.session.data.settings);
	const semester = searchParams.get('semester') || getCurrentSemester(locals.session.data.settings);

	if (cookies.get(consts.TOKEN_COOKIE)) {
		return { participations: getParticipations(fetch, formData, year, semester) };
	}
	return { participations: null };
};