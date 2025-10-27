import { browser } from '$app/environment';
import { loadTranslations } from '$lib/translations';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ url }) => {
  const { pathname } = url;

  let initLocale = 'sk'; // get from cookie, user session, ...

  if (browser) {
    const setLocale = (await cookieStore.get('locale'))?.value;
    if (setLocale) {
      initLocale = setLocale;
    }
    else {
      await cookieStore.set('locale', initLocale);
    }
  }


  await loadTranslations(initLocale, pathname);
};
