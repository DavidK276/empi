<script lang="ts">
	import { t } from '$lib/translations';
	import type { ActionData } from './$types';
	import { goto } from '$app/navigation';
	import { applyAction, enhance } from '$app/forms';
	import { vars } from '$lib/theme.css';
	import { row } from '$lib/style.css';
	import EmailInput from '$lib/components/EmailInput.svelte';

	export let form: ActionData;

	let submitting = false;
	let emails: EmailInput;

	function onFormData(event: FormDataEvent) {
		event.formData.set('email_recipients', emails.getEmails());
	}
</script>

<h1>{$t('research.create_research')}</h1>
<form method="POST" action="?/new"
			on:formdata={onFormData}
			use:enhance={() => {
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
	<EmailInput bind:this={emails}></EmailInput>
	<input type="hidden" name="is_published" value="false">
	<div class="{row} ver-center">
		{#if !submitting}
			<button type="submit">{$t('research.create')}</button>
		{:else}
			<button type="submit" disabled>{$t('research.creating')}</button>
		{/if}
		<div style="display: inline-flex; align-items: center">
			<span class="material-symbols-outlined">info</span>&nbsp;
			{$t('research.creation_info')}
		</div>
		{#if form?.success === false}
			<div style="display: inline-flex; align-items: center; color: {vars.danger}">
				<span class="material-symbols-outlined">error</span>
				{$t('research.error')}
			</div>
		{/if}
	</div>
</form>