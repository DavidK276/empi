<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';

	let submitButton: HTMLButtonElement;

	async function doUpdate() {
		return async ({ update, result }: {
			update: (options?: { reset?: boolean, invalidateAll?: boolean }) => Promise<void>,
			result: ActionResult
		}) => {
			if (result.type === 'success') {
				new FormResultMessage({
					target: submitButton.parentElement as HTMLElement,
					props: { result, message: 'Odkaz bol úspešne odoslaný' }
				});
			}
			else {
				new FormResultMessage({ target: submitButton.parentElement as HTMLElement, props: { result } });
			}
			await update();
		};
	}
</script>

<h1>Pridanie administrátora</h1>
<p class="message">
	<MaterialSymbolsInfoOutline class="icon"></MaterialSymbolsInfoOutline>
	Zadajte emailovú adresu, na ktorú bude doručený odkaz na aktiváciu nového administrátorského účtu.
</p>
<div class="row" style="padding-top: var(--xl);">
	<form method="POST" style="width: 50%" class="m-w-full" use:enhance={doUpdate}>
		<label for="email">Email</label>
		<input type="email" name="email" id="email">
		<div class="row ver-center">
			<button type="submit" bind:this={submitButton}>Odoslať</button>
		</div>
	</form>
</div>