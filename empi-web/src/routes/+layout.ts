import { loadTranslations } from '$lib/translations';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ url }) => {
	const { pathname } = url;

	const initLocale = 'sk'; // get from cookie, user session, ...

	await loadTranslations(initLocale, pathname);
};