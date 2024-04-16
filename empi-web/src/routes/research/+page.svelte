<script lang="ts">
	import { t } from '$lib/translations';
	import type { ActionData } from './$types';
	import { goto } from '$app/navigation';
	import { applyAction, enhance } from '$app/forms';
	import { vars } from '$lib/theme.css';

	export let form: ActionData;

	let submitting = false;
</script>

<h1>{$t('common.research')}</h1>
<form method="POST" action="?/new" use:enhance={() => {
	submitting = true;
	return async ({result}) => {
		if (result.type === 'redirect') {
			await goto(result.location);
		}
		else {
			await applyAction(result);
		}
		submitting = false;
	}
}}>
	<label for="name">{$t('research.name')}</label>
	<input type="text" name="name" id="name" required>
	<label for="info_url">{$t('research.info_url')}</label>
	<input type="url" name="info_url" id="info_url" required>
	<input type="hidden" name="is_published" value="false">
	{#if !submitting}
		<button type="submit">{$t('research.create')}</button>
	{:else}
		<button type="submit" disabled>{$t('research.creating')}</button>
	{/if}
	{#if !form?.success}
		<span style="color: {vars.danger}">{$t('research.error')}</span>
	{/if}
</form>