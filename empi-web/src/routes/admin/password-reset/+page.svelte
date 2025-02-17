<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import { mount } from "svelte";

	let submitButton: HTMLButtonElement;

	async function doUpdate() {
		return async ({ update, result }: {
			update: (options?: { reset?: boolean, invalidateAll?: boolean }) => Promise<void>,
			result: ActionResult
		}) => {
			if (result.type === 'success') {
				mount(FormResultMessage, {
					target: submitButton.parentElement as HTMLElement,
					props: { result, message: 'Odkaz bol úspešne odoslaný' }
				});
			}
			else {
				mount(FormResultMessage, { target: submitButton.parentElement as HTMLElement, props: { result } });
			}
			await update();
		};
	}
</script>

<svelte:options runes={true}></svelte:options>
<h1>Resetovanie hesla</h1>
<div class="row ver-center">
	<MaterialSymbolsInfoOutline class="icon"></MaterialSymbolsInfoOutline>
	Zadajte emailovú adresu používateľa. Pokiaľ používateľ s takou emailovou adresou existuje, bude mu doručený email s
	linkom na obnovu hesla.
</div>
<div class="row" style="padding-top: var(--xl);">
	<form class="m-w-full" method="POST" style="width: 50%" use:enhance={doUpdate}>
		<label for="email">Email</label>
		<input id="email" name="email" type="email">
		<div class="row ver-center">
			<button bind:this={submitButton} type="submit">Odoslať</button>
		</div>
	</form>
</div>