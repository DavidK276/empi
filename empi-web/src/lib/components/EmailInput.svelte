<script lang="ts">
	import AdditionalEmail from '$lib/components/AdditionalEmail.svelte';
	import { onMount } from 'svelte';
	import { t } from "$lib/translations";

	function addNewEmail(event: Event) {
		const target = event.target as HTMLButtonElement;
		const parent = target.parentElement;
		new AdditionalEmail({ target: parent!, anchor: target });
	}

	export function getEmails() {
		const emailInputs = document.getElementsByClassName('email-input');

		const emails: string[] = [];
		for (const elem of emailInputs) {
			const emailInput = elem as HTMLInputElement;
			emails.push(emailInput.value);
		}

		return emails.join(',');
	}

	export function setEmails(emails: string) {
		const separatedEmails = emails.split(',');

		const firstEmail = separatedEmails.shift();
		firstEmailInput.value = firstEmail!;

		if (addEmailButton == null) {
			return;
		}
		for (const email of separatedEmails) {
			new AdditionalEmail({ target: addEmailButton.parentElement!, anchor: addEmailButton, props: { email } });
		}
	}

	export let emails: string = '';
	let addEmailButton: HTMLButtonElement;
	let firstEmailInput: HTMLInputElement;
	onMount(() => setEmails(emails));
</script>

<fieldset>
	<legend>{$t('common.emails')}</legend>
	<div class="row ver-center" style="margin: var(--sm) 0">
		<input type="email" class="email-input" bind:this={firstEmailInput} style="margin: 0">
	</div>
	<button type="button" bind:this={addEmailButton} on:click={addNewEmail}>+</button>
</fieldset>