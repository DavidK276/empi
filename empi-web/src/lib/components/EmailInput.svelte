<script lang="ts">
	import { vars } from '$lib/theme.css';
	import { row } from '$lib/style.css';
	import AdditionalEmail from '$lib/components/AdditionalEmail.svelte';

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
		const firstEmailInput = document.getElementById('first-email-input') as HTMLInputElement;
		firstEmailInput.value = firstEmail!;

		const addEmailButton = document.getElementById('add-email-button');
		if (addEmailButton == null) {
			return;
		}
		for (const email of separatedEmails) {
			new AdditionalEmail({ target: addEmailButton.parentElement!, anchor: addEmailButton, props: { email } });
		}
	}
</script>

<fieldset>
	<legend>Emails</legend>
	<div class="{row} ver-center" style="margin: {vars.sm} 0">
		<input type="email" class="email-input" id="first-email-input" style="margin: 0">
	</div>
	<button type="button" id="add-email-button" on:click={addNewEmail}>+</button>
</fieldset>