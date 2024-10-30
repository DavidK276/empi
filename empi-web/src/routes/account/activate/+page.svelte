<script lang="ts">
	import { t } from "$lib/translations";
	import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import MyLabel from "$lib/components/MyLabel.svelte";
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
					props: { result, message: 'Účet bol aktivovaný. Teraz sa môžete prihlásiť.' }
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
<h1>Aktivácia účtu</h1>
<div class="row" style="padding-top: var(--xl);">
	<form method="POST" style="width: 100%" use:enhance={doUpdate}>
		<label for="email">Email</label>
		<input id="email" name="email" required type="email">
		<div class="row">
			<div class="col" style="width: 50%; gap: 0">
				<label for="first_name">{$t('common.first_name')}</label>
				<input id="first_name" minlength="2" name="first_name" required type="text">
			</div>
			<div class="col" style="width: 50%; gap: 0">
				<label for="last_name">{$t('common.last_name')}</label>
				<input id="last_name" name="last_name" required type="text">
			</div>
		</div>
		<div class="row m-col ver-bottom">
			<div class="col m-w-full" style="width: 50%; gap: 0">
				<MyLabel forId="new_password" hintText={$t('common.password_hint')} icon="warning"
				         labelText={$t('common.password')}></MyLabel>
				<input id="new_password" minlength="8" name="new_password" required type="password">
			</div>
			<div class="col m-w-full" style="width: 50%; gap: 0">
				<label for="repeat_password" title={$t('common.password_hint')}>{$t('common.repeat_password')}</label>
				<input id="repeat_password" minlength="8" required type="password">
			</div>
		</div>
		<div class="row ver-center">
			<button bind:this={submitButton} type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>