<script lang="ts">
	import { t } from '$lib/translations';
	import type { ActionData } from './$types';
	import { goto } from '$app/navigation';
	import { applyAction, enhance } from '$app/forms';
	import EmailInput from '$lib/components/EmailInput.svelte';
	import { addFormErrors } from '$lib/functions';
	import Icon from "@iconify/svelte";

	export let form: ActionData;

	let submitting = false;
	let emails: EmailInput;
</script>

<h1>{$t('research.create_research')}</h1>
<form method="POST" action="?/new"
			on:formdata={(event) => event.formData.set('email_recipients', emails.getEmails())}
			use:enhance={() => {
				submitting = true;
				return async ({result, formElement}) => {
					if (result.type === 'redirect') {
						await goto(result.location);
					}
					else {
						await applyAction(result);
						if (form != null && !form.success) {
							addFormErrors(form.errors, formElement);
						}
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
	<div class="row ver-center">
		{#if !submitting}
			<button type="submit">{$t('research.create')}</button>
		{:else}
			<button type="submit" disabled>{$t('research.creating')}</button>
		{/if}
		<p class="message">
			<Icon icon="material-symbols:info-outline" width="24" height="24"></Icon>&nbsp;
			{$t('research.creation_info')}
		</p>
	</div>
</form>