<script lang="ts">
	import { t } from '$lib/translations';
	import { addFormError, addFormErrors, removeFormError } from '$lib/functions';
	import type { ActionData } from './$types';
	import { applyAction, enhance } from '$app/forms';

	export let form: ActionData;

	const submit = (event: SubmitEvent) => {
		if (passwordInput.value !== repeatPasswordInput.value) {
			addFormError(passwordInput, $t('common.passwords_nomatch'));
			addFormError(repeatPasswordInput, $t('common.passwords_nomatch'));
			event.preventDefault();
			event.stopPropagation();
			event.stopImmediatePropagation();
		}
		else {
			removeFormError(passwordInput);
			removeFormError(repeatPasswordInput);
		}
	};

	let submitting = false;
	let passwordInput: HTMLInputElement;
	let repeatPasswordInput: HTMLInputElement;
</script>

<h1>{$t('common.registration')}</h1>
<form method="POST" id="register_form"
      on:submit={submit}
      use:enhance={() => {
				submitting = true;
				return async ({result, formElement}) => {
					await applyAction(result);
					if (form != null && !form.success) {
							addFormErrors(form.errors, formElement);
					}
					submitting = false;
				}
			}}>
	<label for="email">Email</label>
	<input type="email" name="email" id="email" required style="width: 50%" class="m-w-full">
	<p class="error-msg">{$t('common.username_wrong')}</p>
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
			<label for="password">{$t('common.password')}</label>
			<input type="password" name="password" id="password" required minlength="8" bind:this={passwordInput}>
		</div>
		<div class="col m-w-full" style="width: 50%; gap: 0">
			<label for="repeat_password" title={$t('common.password_hint')}>{$t('common.repeat_password')}</label>
			<input type="password" id="repeat_password" required minlength="8" bind:this={repeatPasswordInput}>
		</div>
	</div>
	{#if !submitting}
		<button type="submit" name="submit">{$t('common.register')}</button>
	{:else}
		<button type="submit" disabled>{$t('common.registering')}</button>
	{/if}
	{#if form?.success}
		<span style="color: var(--success)">{$t('common.registration_ok')}</span>
	{/if}
</form>