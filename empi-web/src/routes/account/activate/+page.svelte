<script lang="ts">
	import { t } from "$lib/translations";
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import MyLabel from "$lib/components/MyLabel.svelte";

	let submitButton: HTMLButtonElement;

	async function doUpdate() {
		return async ({ update, result }: {
			update: (options?: { reset?: boolean, invalidateAll?: boolean }) => Promise<void>,
			result: ActionResult
		}) => {
			if (result.type === 'success') {
				new FormResultMessage({
					target: submitButton.parentElement as HTMLElement,
					props: { result, message: 'Účet bol aktivovaný. Teraz sa môžete prihlásiť.' }
				});
			}
			else {
				new FormResultMessage({ target: submitButton.parentElement as HTMLElement, props: { result } });
			}
			await update();
		};
	}
</script>

<h1>Aktivácia účtu</h1>
<div class="row" style="padding-top: var(--xl);">
	<form method="POST" style="width: 100%" use:enhance={doUpdate}>
		<label for="email">Email</label>
		<input type="email" name="email" id="email" required>
		<div class="row">
			<div class="col" style="width: 50%; gap: 0">
				<label for="first_name">{$t('common.first_name')}</label>
				<input type="text" name="first_name" id="first_name" required minlength="2">
			</div>
			<div class="col" style="width: 50%; gap: 0">
				<label for="last_name">{$t('common.last_name')}</label>
				<input type="text" name="last_name" id="last_name" required>
			</div>
		</div>
		<div class="row m-col ver-bottom">
			<div class="col m-w-full" style="width: 50%; gap: 0">
				<MyLabel forId="new_password" labelText={$t('common.password')} hintText={$t('common.password_hint')}
				         icon="warning"></MyLabel>
				<input type="password" name="new_password" id="new_password" required minlength="8">
			</div>
			<div class="col m-w-full" style="width: 50%; gap: 0">
				<label for="repeat_password" title={$t('common.password_hint')}>{$t('common.repeat_password')}</label>
				<input type="password" id="repeat_password" required minlength="8">
			</div>
		</div>
		<div class="row ver-center">
			<button type="submit" bind:this={submitButton}>{$t('common.submit')}</button>
		</div>
	</form>
</div>