<script lang="ts">
	import { t } from '$lib/translations';
	import type { ActionData } from './$types';
	import { goto } from '$app/navigation';
	import { applyAction, enhance } from '$app/forms';
	import EmailInput from '$lib/components/EmailInput.svelte';
	import { addFormErrors } from '$lib/functions';
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import { onMount } from "svelte";
	import { base } from "$app/paths";

	let { form }: { form: ActionData } = $props();

	let submitting = $state(false);
	let emails: EmailInput;

	onMount(() => {
		if (!$page.data.user?.is_staff) {
			goto(`${base}/`, { replaceState: true });
		}
	});
</script>

<h1>{$t('research.create_research')}</h1>
<form action="?/new" method="POST"
      onformdata={(event) => event.formData.set('email_recipients', emails.getEmails())}
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
	<input id="name" name="name" required type="text">
	<EmailInput bind:this={emails}></EmailInput>
	<input name="is_published" type="hidden" value="false">
	<div class="row ver-center">
		{#if !submitting}
			<button type="submit">{$t('research.create')}</button>
		{:else}
			<button type="submit" disabled>{$t('research.creating')}</button>
		{/if}
		<p class="message">
			<MaterialSymbolsInfoOutline height="24" width="24"></MaterialSymbolsInfoOutline>&nbsp;
			{$t('research.creation_info')}
		</p>
	</div>
</form>