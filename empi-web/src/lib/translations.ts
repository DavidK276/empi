import type { Config } from 'sveltekit-i18n';
import i18n from 'sveltekit-i18n';

const config: Config = {
	loaders: [
		{
			locale: 'en',
			key: 'common',
			loader: async () => (
				await import('./en/common.json')
			).default
		},
		{
			locale: 'en',
			key: 'attrs',
			routes: ['/attributes', /\/research.*/], // you can use regexes as well!
			loader: async () => (
				await import('./en/attrs.json')
			).default
		},
		{
			locale: 'en',
			key: 'account',
			routes: ['/account'], // you can use regexes as well!
			loader: async () => (
				await import('./en/account.json')
			).default
		},
		{
			locale: 'en',
			key: 'research',
			routes: [/\/research.*/], // you can use regexes as well!
			loader: async () => (
				await import('./en/research.json')
			).default
		},
		{
			locale: 'sk',
			key: 'common',
			loader: async () => (
				await import('./sk/common.json')
			).default
		},
		{
			locale: 'sk',
			key: 'attrs',
			routes: ['/attributes', /\/research.*/], // you can use regexes as well!
			loader: async () => (
				await import('./sk/attrs.json')
			).default
		},
		{
			locale: 'sk',
			key: 'account',
			routes: ['/account'], // you can use regexes as well!
			loader: async () => (
				await import('./sk/account.json')
			).default
		},
		{
			locale: 'sk',
			key: 'research',
			routes: [/\/research.*/], // you can use regexes as well!
			loader: async () => (
				await import('./sk/research.json')
			).default
		}
	]
};

export const { t, locale, locales, loading, loadTranslations } = new i18n(config);