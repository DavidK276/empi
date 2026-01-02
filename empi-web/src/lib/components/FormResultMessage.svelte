<script lang="ts">
	import { t } from '$lib/translations';
	import MaterialSymbolsErrorOutline from 'virtual:icons/material-symbols/error-outline';
	import type { ActionResult } from "@sveltejs/kit";
	import { onMount } from "svelte";

	let props: { message?: string | null, result?: ActionResult | null } = $props();
	let message = $state(props.message);
	const result = props.result;

	onMount(() => {
		if (!message && result) {
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
		if (message) {
					message = message.charAt(0).toUpperCase() + message.slice(1);
		}
	})

	// destroys all previous messages before adding new one
	$effect.pre(() => {
		document.querySelectorAll('.form-result').forEach(element => element.remove());
	});
</script>

<div class="form-result">
	{#if result && (result.type === 'error' || result.type === 'failure')}
		<p style="color: var(--danger)">
			<MaterialSymbolsErrorOutline width="24" height="24"></MaterialSymbolsErrorOutline>&nbsp;{message}</p>
	{:else}
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
