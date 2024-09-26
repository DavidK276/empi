<script lang="ts">
	import { t } from "$lib/translations";
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
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
					props: { result, message: 'Heslo bolo obnovené. Teraz sa môžete prihlásiť.' }
				});
			}
			else {
				new FormResultMessage({ target: submitButton.parentElement as HTMLElement, props: { result } });
			}
			await update();
		};
	}
</script>

<h1>Resetovanie hesla</h1>
<div class="row" style="padding-top: var(--xl);">
	<form method="POST" style="width: 50%" class="m-w-full" use:enhance={doUpdate}>
		<label for="new_password">Nové heslo</label>
		<input type="password" name="new_password" id="new_password">
		<label for="repeat_password">{$t('common.repeat_password')}</label>
		<input type="password" id="repeat_password">
		<div class="row ver-center">
			<button type="submit" bind:this={submitButton}>{$t('common.submit')}</button>
		</div>
	</form>
</div>