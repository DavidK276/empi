<script lang="ts">
	import { t } from '$lib/translations';
	import MaterialSymbolsErrorOutline from 'virtual:icons/material-symbols/error-outline';

	export let type: string;
	export let message: string = '';

	if (!message) {
		if (type === 'error' || type === 'failure') {
			message = $t('common.unknown_error');
		}
		else if (type === 'success') {
			message = $t('common.saved');
		}
	}

	// destroys all previous messages before adding new one
	document.querySelectorAll('.form-result').forEach(element => element.remove());
</script>

<div class="form-result">
	{#if type === 'error' || type === 'failure'}
		<p style="color: var(--danger)"><MaterialSymbolsErrorOutline width="24" height="24"></MaterialSymbolsErrorOutline>&nbsp;{message}</p>
	{:else if type === 'success'}
		<p style="color: var(--success)">{message}</p>
	{/if}
</div>

<style>
    p {
        display: inline-flex;
        margin: 0;
    }

		div {
				display: inline-flex;
		}
</style>