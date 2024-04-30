import type { LayoutServerLoad } from './$types';


export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		user: locals.user,
		participant: locals.participant,
		research_auth: locals.session.data.research_password != null
	};
};