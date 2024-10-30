<script lang="ts">
	import { t } from "$lib/translations";
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import { mount } from "svelte";
	import { addFormError, removeFormError } from "$lib/functions";

	let submitButton: HTMLButtonElement;
	let passwordInput: HTMLInputElement;
	let repeatPasswordInput: HTMLInputElement;

	async function doUpdate() {
		return async ({ update, result }: {
			update: (options?: { reset?: boolean, invalidateAll?: boolean }) => Promise<void>,
			result: ActionResult
		}) => {
			if (result.type === 'success') {
				mount(FormResultMessage, {
					target: submitButton.parentElement as HTMLElement,
					props: { result, message: 'Heslo bolo obnovené. Teraz sa môžete prihlásiť.' }
				});
			}
			else {
				mount(FormResultMessage, { target: submitButton.parentElement as HTMLElement, props: { result } });
			}
			await update();
		};
	}

	const submit = (event: SubmitEvent) => {
		if (passwordInput.value !== repeatPasswordInput.value) {
			addFormError(passwordInput, $t('common.passwords_nomatch'));
			addFormError(repeatPasswordInput, $t('common.passwords_nomatch'));
			event.preventDefault();
			event.stopPropagation();
		}
		else {
			removeFormError(passwordInput);
			removeFormError(repeatPasswordInput);
		}
	};
</script>

<h1>Resetovanie hesla</h1>
<div class="row" style="padding-top: var(--xl);">
	<form class="m-w-full" method="POST" onsubmit={submit} style="width: 50%" use:enhance={doUpdate}>
		<label for="new_password">Nové heslo</label>
		<input bind:value={passwordInput} id="new_password" name="new_password" type="password">
		<label for="repeat_password">{$t('common.repeat_password')}</label>
		<input bind:value={repeatPasswordInput} id="repeat_password" type="password">
		<div class="row ver-center">
			<button bind:this={submitButton} type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>