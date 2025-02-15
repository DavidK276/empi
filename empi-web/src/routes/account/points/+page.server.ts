import * as consts from "$lib/constants";
import { INT_API_ENDPOINT } from "$lib/constants";
import type { IParticipation } from "$lib/objects/participation";
import type { PageServerLoad } from "./$types";
import { getCurrentAcademicYear, getCurrentSemester } from "$lib/settings";

// eslint-disable-next-line @typescript-eslint/no-unsafe-function-type
async function loadParticipations(fetch: Function, formData: FormData, year: string, semester: string) {
	const response = await fetch(consts.INT_API_ENDPOINT + `participation/user/?year=${year}&semester=${semester}`, {
		body: formData,
		method: 'POST'
	});
	const responseJSON = await response.json();

	const participations: IParticipation[] = [];
	for (const participation of responseJSON) {
		participations.push(participation);
	}
	return participations;
}

export const load: PageServerLoad = async ({ cookies, fetch, locals, request }) => {

	const response = await fetch(INT_API_ENDPOINT + 'participation/academic_year_choices/');
	const academic_year_choices = await response.json();

	const formData = new FormData();
	formData.set('password', locals.session.data.user_password);
	if (cookies.get(consts.TOKEN_COOKIE)) {
		const searchParams = new URL(request.url).searchParams;
		const year = searchParams.get('year') || getCurrentAcademicYear(locals.session.data.settings);
		const semester = searchParams.get('semester') || getCurrentSemester(locals.session.data.settings);


		return { participations: loadParticipations(fetch, formData, year, semester), academic_year_choices }
	}
	return { participations: null, academic_year_choices }
}