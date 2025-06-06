import type { Config } from 'sveltekit-i18n';
import i18n from 'sveltekit-i18n';
import { base } from "$app/paths";

const config: Config = {
	loaders: [
		{
			locale: 'en',
			key: 'common',
			loader: async () => (
				await import('./translations/en/common.json')
			).default
		},
		{
			locale: 'en',
			key: 'attrs',
			routes: [`${base}/attributes`, RegExp(`${base}/research/.*`)], // you can use regexes as well!
			loader: async () => (
				await import('./translations/en/attrs.json')
			).default
		},
		{
			locale: 'en',
			key: 'account',
			routes: [`${base}/account`],
			loader: async () => (
				await import('./translations/en/account.json')
			).default
		},
		{
			locale: 'en',
			key: 'research',
			loader: async () => (
				await import('./translations/en/research.json')
			).default
		},
		{
			locale: 'sk',
			key: 'common',
			loader: async () => (
				await import('./translations/sk/common.json')
			).default
		},
		{
			locale: 'sk',
			key: 'attrs',
			routes: [`${base}/attributes`, RegExp(`${base}/research/.*`)], // you can use regexes as well!
			loader: async () => (
				await import('./translations/sk/attrs.json')
			).default
		},
		{
			locale: 'sk',
			key: 'account',
			routes: [`${base}/account`], // you can use regexes as well!
			loader: async () => (
				await import('./translations/sk/account.json')
			).default
		},
		{
			locale: 'sk',
			key: 'research',
			loader: async () => (
				await import('./translations/sk/research.json')
			).default
		}
	]
};

export const { t, locale, locales, loading, loadTranslations } = new i18n(config);