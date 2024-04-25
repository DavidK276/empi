<script lang="ts">
	import { vars } from '$lib/theme.css';
	import { row } from '$lib/style.css';
	import AdditionalEmail from '$lib/components/AdditionalEmail.svelte';

	function addNewEmail(event: Event) {
		const target = event.target as HTMLButtonElement;
		const parent = target.parentElement;
		new AdditionalEmail({target: parent!, anchor: target});
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
</script>

<fieldset>
	<legend>Emails</legend>
	<div class="{row} ver-center" style="margin: {vars.sm} 0">
		<input type="email"  class="email-input" style="margin: 0">
	</div>
	<button type="button" on:click={addNewEmail}>+</button>
</fieldset>