<script lang="ts">
	import { t } from '$lib/translations.js';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import type { ActionResult } from "@sveltejs/kit";
	import { base } from "$app/paths";
	import FormResultMessage from "$lib/components/FormResultMessage.svelte";

	async function login() {
		logging_in = true;

		return async ({ update, result }: { update: () => Promise<void>, result: ActionResult }) => {
			await update();
			logging_in = false;
			console.log(result);
			if (result.type === 'success') {
				is_logged_in = true;
				login_message = "";
			}
			if (result.status === 401) {
				is_logged_in = false;
				login_message = $t('common.wrong_login');
			}
			else if (result.type === 'failure') {
				new FormResultMessage({ target: document.getElementById('submitBtn')!, props: { result } })
			}
		};
	}

	export let is_logged_in: boolean;
	let logging_in = false;
	let logging_out = false;

	let login_message = "";
</script>
{#if !is_logged_in}
	<form method="POST" action="{base}/?/login" style="width: 100%"
	      use:enhance={login}>
		<label for="email">Email: </label>
		<input type="email" id="email" name="email" required>
		<label for="password">{$t('common.password')}: </label>
		<input type="password" id="password" name="password" required>
		{#if login_message}
			<p class="error-msg" style="display: block; margin-top: 0">{login_message}</p>
		{/if}
		<div style="display: flex; flex-wrap: nowrap">
			{#if logging_in}
				<button type="submit" disabled>{$t('common.logging_in')}</button>
			{:else}
				<button type="submit" id="loginBtn">{$t('common.login')}</button>
			{/if}
			<a href="{base}/account/register" style="margin: 0 var(--sm)">{$t('common.registration')}</a>
		</div>
	</form>
{:else}
	<form method="POST" action="{base}/?/logout"
	      use:enhance={() => {
									logging_out = true;

									return async ({ update }) => {
										await goto(`${base}/`);
										await update();
										logging_out = false;
										is_logged_in = false;
									};
								}}>
		{#if logging_out}
			<button type="submit" disabled>{$t('common.logging_out')}</button>
		{:else}
			<button type="submit">{$t('common.logout')}</button>
		{/if}
	</form>
{/if}