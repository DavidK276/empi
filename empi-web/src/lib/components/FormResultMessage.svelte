<script lang="ts">
	import { t } from '$lib/translations';
	import MaterialSymbolsErrorOutline from 'virtual:icons/material-symbols/error-outline';
	import type { ActionResult } from "@sveltejs/kit";

	export let message: string = '';
	export let result: ActionResult;

	if (!message) {
		if (result.type === 'error') {
			message = $t('common.unknown_error');
		}
		else if (result.type === 'success') {
			message = $t('common.saved');
		}
		else if (result.type === 'failure') {
			const errors = result.data?.errors;

			if (errors.non_field_errors != null && errors.non_field_errors.length > 0) {
				message = errors.non_field_errors[0];
			}
			if (errors.detail != null) {
				message = errors.detail;
			}
		}
	}

	message = message.charAt(0).toUpperCase() + message.slice(1);

	// destroys all previous messages before adding new one
	document.querySelectorAll('.form-result').forEach(element => element.remove());
</script>

<div class="form-result">
	{#if result.type  === 'error' || result.type  === 'failure'}
		<p style="color: var(--danger)"><MaterialSymbolsErrorOutline width="24" height="24"></MaterialSymbolsErrorOutline>&nbsp;{message}</p>
	{:else if result.type  === 'success'}
		<p style="color: var(--success)">{message}</p>
	{/if}
</div>

<style>
    p {
        display: inline-flex;
		    align-items: center;
        margin: 0;
    }

		div {
				display: inline-flex;
		}
</style>