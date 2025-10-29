<script lang="ts">
	import { t } from '$lib/translations';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import type { ActionResult } from "@sveltejs/kit";
	import { resolve } from "$app/paths";
	import FormResultMessage from "$lib/components/FormResultMessage.svelte";
	import { mount } from "svelte";

	async function login() {
		logging_in = true;

		return async ({ update, result }: { update: () => Promise<void>, result: ActionResult }) => {
			await update();
			logging_in = false;
			if (result.type === 'success') {
				is_logged_in = true;
				login_message = "";
			}
			if (result.status === 401) {
				is_logged_in = false;
				login_message = $t('common.wrong_login');
			}
			else if (result.type === 'failure') {
				mount(FormResultMessage, { target: document.getElementById('submitBtn')!, props: { result } })
			}
		};
	}

	let { is_logged_in }: { is_logged_in: boolean } = $props();
	let logging_in = $state(false);
	let logging_out = $state(false);

	let login_message = $state("");
</script>
{#if !is_logged_in}
	<form method="POST" action="{resolve('/')}?/login" style="width: 100%"
	      use:enhance={login}>
		<label for="email">Email: </label>
		<input type="email" id="email" name="email" required>
		<label for="password">{$t('common.password')}: </label>
		<input type="password" id="password" name="password" required>
		{#if login_message}
			<div class="error-msg" style="margin-top: 0">{login_message}</div>
		{/if}
		<div style="display: flex; flex-wrap: nowrap">
			{#if logging_in}
				<button type="submit" disabled>{$t('common.logging_in')}</button>
			{:else}
				<button type="submit" id="loginBtn">{$t('common.login')}</button>
			{/if}
			<a href="{resolve('/account/register')}" style="margin: 0 var(--sm)">{$t('common.registration')}</a>
		</div>
	</form>
{:else}
	<form method="POST" action="{resolve('/')}?/logout"
	      use:enhance={() => {
									logging_out = true;

									return async ({ update }) => {
										await goto(resolve('/'));
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
