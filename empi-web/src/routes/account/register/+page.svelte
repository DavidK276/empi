<script lang="ts">
	import { t } from '$lib/translations';
	import { addFormError, removeFormError } from '$lib/functions';
	import type { ActionData } from './$types';
	import { enhance } from '$app/forms';
	import { universalEnhance } from "$lib/enhanceFunctions";

	let { form }: { form: ActionData } = $props();

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

	let passwordInput: HTMLInputElement;
	let repeatPasswordInput: HTMLInputElement;
</script>

<h1>{$t('common.registration')}</h1>
<form id="register_form" method="POST" onsubmit={submit}
      use:enhance={({formElement, submitter}) => {
				return universalEnhance({formElement, submitter}, {
					idleMessage: $t('common.register'),
					runningMessage: $t('common.registering'),
					reset: true,
					invalidateAll: false,
					printSuccessMessage: false
				});
			}}>
	<label for="email">Email</label>
	<input class="m-w-full" id="email" name="email" required style="width: 50%" type="email">
	<p class="error-msg">{$t('common.username_wrong')}</p>
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
			<label for="password">{$t('common.password')}</label>
			<input bind:this={passwordInput} id="password" minlength="8" name="password" required type="password">
		</div>
		<div class="col m-w-full" style="width: 50%; gap: 0">
			<label for="repeat_password" title={$t('common.password_hint')}>{$t('common.repeat_password')}</label>
			<input bind:this={repeatPasswordInput} id="repeat_password" minlength="8" required type="password">
		</div>
	</div>
	<div class="row ver-center" id="submit-div">
		<button type="submit">{$t('common.register')}</button>
		{#if form?.success}
			<span style="color: var(--success)">{$t('common.registration_ok')}</span>
		{/if}
	</div>
</form>