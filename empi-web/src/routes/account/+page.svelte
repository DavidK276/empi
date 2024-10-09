<script lang="ts">
	import { t } from '$lib/translations';
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import MaterialSymbolsHelpOutline from 'virtual:icons/material-symbols/help-outline';
	import type { ActionResult } from "@sveltejs/kit";
	import { addFormErrors } from "$lib/functions";
	import FormResultMessage from "$lib/components/FormResultMessage.svelte";

	let user = $page.data.user;
	let participant = $page.data.participant;

	async function doUpdate({ formElement }: { formElement: HTMLFormElement }) {
		return async ({ update, result }: {
			update: (options?: { reset?: boolean, invalidateAll?: boolean }) => Promise<void>,
			result: ActionResult
		}) => {
			const submitDiv = formElement.children.namedItem('submit-div');
			if (submitDiv != null) {
				new FormResultMessage({target: submitDiv, props: {result}});
			}
			if (result.type === 'failure') {
				addFormErrors(result.data?.errors, formElement);
			}
			await update({ reset: false });
		};
	}
</script>
<div class="row ver-center">
	<h1>{$t('account.my_account')}</h1>
	{#if user?.is_staff}
		<button style="background-color: var(--danger)">Superuser</button>
	{:else}
		<button>Participant</button>
	{/if}
</div>
<h2>{$t('account.personal_info')}</h2>
<div class="col">
	{#if participant != null}
		<div class="col">
			<label for="token" title={$t('common.token_hint')}>Token&nbsp;
				<MaterialSymbolsHelpOutline width="24" height="24"></MaterialSymbolsHelpOutline>
			</label>
			<button id="token" style="font-size: 18px">{participant.token}</button>
		</div>
	{/if}
	<form method="POST" action="?/updateInfo" use:enhance={doUpdate}>
		<div class="row">
			<div style="width: 50%">
				<label for="first_name">{$t('common.first_name')}</label>
				<input type="text" id="first_name" name="first_name" value={user?.first_name}>
			</div>
			<div style="width: 50%">
				<label for="last_name">{$t('common.last_name')}</label>
				<input type="text" id="last_name" name="last_name" value={user?.last_name}>
			</div>
		</div>
		<div class="row">
			<div style="width: 100%">
				<label for="email">Email</label>
				<input type="email" id="email" name="email" value={user?.email}>
			</div>
		</div>
		<div class="row ver-center" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>
<h2>{$t('account.password_change')}</h2>
<div class="col">
	<form method="POST" action="?/changePassword" use:enhance={doUpdate}>
		<div class="row">
			<div style="width: 50%">
				<label for="current_password">{$t('common.current_password')}</label>
				<input type="password" id="current_password" name="current_password" minlength="8">
			</div>
			<div style="width: 50%">
				<label for="new_password">{$t('common.new_password')}</label>
				<input type="password" id="new_password" name="new_password" minlength="8">
			</div>
		</div>
		<div class="row ver-center" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>