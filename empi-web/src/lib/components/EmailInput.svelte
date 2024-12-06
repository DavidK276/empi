<script lang="ts">
	import AdditionalEmail from '$lib/components/AdditionalEmail.svelte';
	import { mount, onMount } from 'svelte';
	import { t } from "$lib/translations";

	function addNewEmail(event: Event) {
		const target = event.target as HTMLButtonElement;
		const parent = target.parentElement;
		mount(AdditionalEmail, { target: parent!, anchor: target });
	}

	export function getEmails() {
		const emailInputs = document.getElementsByClassName('email-input');

		const emails: string[] = [];
		for (const elem of emailInputs) {
			const emailInput = elem as HTMLInputElement;
			const value = emailInput.value.trim();
			if (value) {
				emails.push(value);
			}
		}

		return emails.join(',');
	}

	export function setEmails(emails: string) {
		const separatedEmails = emails.split(',');

		const firstEmail = separatedEmails.shift();
		firstEmailInput.value = firstEmail!;

		for (const email of separatedEmails) {
			mount(AdditionalEmail, { target: addEmailButton.parentElement!, anchor: addEmailButton, props: { email } });
		}
	}

	let { emails = '' } = $props();
	let addEmailButton: HTMLButtonElement;
	let firstEmailInput: HTMLInputElement;
	onMount(() => setEmails(emails));
</script>

<fieldset>
	<legend>{$t('common.emails')}</legend>
	<div class="row ver-center" style="margin: var(--sm) 0">
		<input bind:this={firstEmailInput} class="email-input" type="email">
	</div>
	<button bind:this={addEmailButton} onclick={addNewEmail} type="button">+</button>
</fieldset>