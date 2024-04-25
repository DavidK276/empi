<script lang="ts">
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';

	export let type: string;
	export let message: string = '';

	if (!message) {
		if (type === 'error' || type === 'failure') {
			message = $t('common.unknown_error');
		}
		else if (type === 'success') {
			message = $t('common.saved')
		}
	}
</script>

{#if type === 'error' || type === 'failure'}
	<p style="color: {vars.danger}"><span
		class="material-symbols-outlined">error</span>&nbsp;{message}</p>
{:else if type === 'success'}
	<p style="color: {vars.success}">{message}</p>
{/if}

<style>
	p {
			display: inline-flex;
			margin: 0;
	}
</style>