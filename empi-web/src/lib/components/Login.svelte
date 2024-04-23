<script lang="ts">
	import { t } from '$lib/translations.js';
	import { page } from '$app/stores';
	import { error } from '$lib/style.css.js';
	import { vars } from '$lib/theme.css.js';
	import { enhance } from '$app/forms';
	import { store } from '$lib/stores.js';
	import { goto } from '$app/navigation';

	function setPasswordSession(event: Event) {
		const form = event.target as HTMLFormElement;
		const passwordInput = form.elements.namedItem('password') as HTMLInputElement;
		$store.password = passwordInput?.value;
	}

	function unsetPasswordSession() {
		$store.password = '';
	}

	export let is_logged_in: boolean;
	let logging_in = false;
	let logging_out = false;
</script>
{#if !is_logged_in}
	<form method="POST" action="/?/login" style="width: 100%" on:submit={setPasswordSession}
				use:enhance={() => {
									logging_in = true;

									return async ({ update, result }) => {
										await update();
										logging_in = false;
										is_logged_in = true;
									};
								}}>
		<label for="username">{$t('common.username')}: </label>
		<input type="text" id="username" name="username" required>
		<label for="password">{$t('common.password')}: </label>
		<input type="password" id="password" name="password" required minlength="4">
		{#if $page.form?.login === false}
			<p class="{error}" style="white-space: nowrap">{$t('common.wrong_login')}</p>
		{/if}
		<div style="display: flex; flex-wrap: nowrap">
			{#if logging_in}
				<button type="submit" disabled>{$t('common.logging_in')}</button>
			{:else}
				<button type="submit" id="submit">{$t('common.login')}</button>
			{/if}
			<a href="/register" style="margin: 0 {vars.sm}">{$t('common.registration')}</a>
		</div>
	</form>
{:else}
	<form method="POST" action="/?/logout" on:submit={unsetPasswordSession}
				use:enhance={() => {
									logging_out = true;

									return async ({ update }) => {
										await update();
										await goto("/");
										logging_out = false;
										is_logged_in = false;
									};
								}}>
		{#if logging_out}
			<button type="submit" disabled>{$t('common.logging_out')}</button>
		{:else}
			<button type="submit" name="submit">{$t('common.logout')}</button>
		{/if}
	</form>
{/if}