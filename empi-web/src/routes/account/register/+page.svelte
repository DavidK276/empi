<script lang="ts">
	import { t } from '$lib/translations';
	import { addFormError, addFormErrors, removeFormError } from '$lib/functions';
	import type { ActionData } from './$types';
	import { onMount } from 'svelte';
	import { vars } from '$lib/theme.css';

	export let form: ActionData;

	const verifyForm = (form: HTMLFormElement) => {
		let result = true;
		const passwordInput = form.elements.namedItem('password') as HTMLInputElement;
		const repeatPasswordInput = form.elements.namedItem('repeat_password') as HTMLInputElement;
		if (passwordInput.value != repeatPasswordInput.value) {
			addFormError(passwordInput, $t('common.passwords_nomatch'));
			addFormError(repeatPasswordInput, $t('common.passwords_nomatch'));
			result = false;
		}
		else {
			removeFormError(passwordInput);
			removeFormError(repeatPasswordInput);
		}

		const usernameInput = form.elements.namedItem('username') as HTMLInputElement;
		if (!/^[a-zA-Z0-9]+$/.test(usernameInput.value)) {
			addFormError(usernameInput, $t('common.username_wrong'));
			result = false;
		}
		else {
			removeFormError(usernameInput);
		}
		return result;
	};

	const formCheck = (event: Event) => {
		const target = event.target as HTMLElement;
		const formElement = target.parentElement as HTMLFormElement;
		const submitButton = formElement.children.namedItem('submit');
		if (formElement.checkValidity() && verifyForm(formElement)) {
			submitButton?.removeAttribute('disabled');
		}
		else {
			submitButton?.setAttribute('disabled', '');
		}
	};

	onMount(() => {
		const formElement = document.getElementById('register_form') as HTMLFormElement;
		if (form?.success === false) {
			addFormErrors(form.errors, formElement);
		}
	});
</script>

<h1>{$t('common.registration')}</h1>
<form method="POST" id="register_form" on:input={formCheck}>
	<label for="username" title={$t('common.username_hint')}>
		{$t('common.username')}
		<span class="material-symbols-outlined">help</span>
	</label>
	<input type="text" name="username" id="username" required>
	<label for="first_name">{$t('common.first_name')}</label>
	<input type="text" name="first_name" id="first_name" required>
	<label for="last_name">{$t('common.last_name')}</label>
	<input type="text" name="last_name" id="last_name" required>
	<label for="email">Email</label>
	<input type="email" name="email" id="email" required>
	<label for="password" title={$t('common.password_hint')}>
		{$t('common.password')}
		<span class="material-symbols-outlined">warning</span>
	</label>
	<input type="password" name="password" id="password" required minlength="8">
	<label for="repeat_password" title={$t('common.password_hint')}>{$t('common.repeat_password')}</label>
	<input type="password" id="repeat_password" required minlength="8">
	<button type="submit" name="submit" disabled>{$t('common.register')}</button>
	{#if form?.success}
		<span style="color: {vars.success}">{$t('common.registration_ok')}</span>
	{/if}
</form>