import { persistent } from '@furudean/svelte-persistent-store';

export const store = persistent({
	start_value: {
		user_password: '',
		research_password: ''
	},
	key: 'empi:store',
	storage_type: 'sessionStorage'
});