<script lang="ts">
	import { t } from '$lib/translations';
	import { col, row } from '$lib/style.css';
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import Icon from "@iconify/svelte";

	let user = $page.data.user;
	let participant = $page.data.participant;
</script>
<div class="{row} ver-center">
	<h1>{$t('account.my_account')}</h1>
	{#if user?.is_staff}
		<button style="background-color: var(--danger)">Superuser</button>
	{:else}
		<button>Participant</button>
	{/if}
</div>
<h2>{$t('account.personal_info')}</h2>
<div class={col}>
	{#if participant != null}
		<div class={col}>
			<label for="token" title={$t('common.token_hint')}>Token&nbsp;
				<Icon icon="material-symbols:help-outline" width="24" height="24"></Icon>
			</label>
			<button id="token" style="font-size: 18px">{participant.token}</button>
		</div>
	{/if}
	<form method="POST" use:enhance={({formElement}) => {
		return async ({update, result}) => {
			const submitDiv = formElement.children.namedItem('submit-div');
			if (submitDiv != null) {
				new FormResultMessage({target: submitDiv, props: {type: result.type}});
			}
			await update({reset: false});
		};
	}}>
		<div class={row}>
			<div style="width: 50%">
				<label for="first_name">{$t('common.first_name')}</label>
				<input type="text" id="first_name" name="first_name" value={user?.first_name}>
			</div>
			<div style="width: 50%">
				<label for="last_name">{$t('common.last_name')}</label>
				<input type="text" id="last_name" name="last_name" value={user?.last_name}>
			</div>
		</div>
		<div class={row}>
			<div style="width: 50%">
				<label for="username">{$t('common.username')}</label>
				<input type="text" id="username" readonly value={user?.username}>
			</div>
			<div style="width: 50%">
				<label for="email">Email</label>
				<input type="email" id="email" name="email" value={user?.email}>
			</div>
		</div>
		<div class="{row} ver-center" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>