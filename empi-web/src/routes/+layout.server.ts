import type { LayoutServerLoad } from './$types';


export const load: LayoutServerLoad = async ({ locals, cookies }) => {
	return {
		session: locals.session.data,
		user: locals.session.data.user,
		participant: locals.session.data.participant,
		research_auth: locals.session.data.research_password != null,
		settings: locals.session.data.settings,
		locale: cookies.get('locale')
	};
};
