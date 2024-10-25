<script lang="ts">
	import { t } from '$lib/translations';
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import { universalEnhance } from '$lib/enhanceFunctions';
	import MaterialSymbolsHelpOutline from 'virtual:icons/material-symbols/help-outline';

	const user = $page.data.user;
	const participant = $page.data.participant;

	const onTokenButtonClick = (event: MouseEvent) => {
		navigator.clipboard.writeText(participant.token);
		const target = event.target as HTMLButtonElement;
		target.innerText = "Skopírovaný!"
		setTimeout(() => {
			target.innerText = participant.token
		}, 1000);
	};
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
			<label for="token" title={$t('common.token_hint')}>{$t('common.token')}&nbsp;({$t('common.click_to_copy')}
				)&nbsp;
				<MaterialSymbolsHelpOutline width="24" height="24"></MaterialSymbolsHelpOutline>
			</label>
			<button id="token" style="font-size: 18px; cursor: pointer" title="{$t('common.click_to_copy')}"
			        on:click={onTokenButtonClick}>{participant.token}</button>
		</div>
	{/if}
	<form action="?/updateInfo" method="POST" use:enhance={({formElement, submitter}) => {
		return universalEnhance({formElement, submitter}, {
			idleMessage: $t('common.submit'),
			runningMessage: $t('common.submitting'),
			reset: false,
			invalidateAll: true
		});
	}}>
		<div class="row">
			<div style="width: 50%">
				<label for="first_name">{$t('common.first_name')}</label>
				<input id="first_name" name="first_name" type="text" value={user?.first_name}>
			</div>
			<div style="width: 50%">
				<label for="last_name">{$t('common.last_name')}</label>
				<input id="last_name" name="last_name" type="text" value={user?.last_name}>
			</div>
		</div>
		<div class="row">
			<div style="width: 100%">
				<label for="email">Email</label>
				<input id="email" name="email" type="email" value={user?.email}>
			</div>
		</div>
		<div class="row ver-center" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>
<h2>{$t('account.password_change')}</h2>
<div class="col">
	<form action="?/changePassword" method="POST" use:enhance={({formElement, submitter}) => {
		return universalEnhance({formElement, submitter}, {
			idleMessage: $t('common.submit'),
			runningMessage: $t('common.submitting'),
			reset: false,
			invalidateAll: false
		});
	}}>
		<div class="row">
			<div style="width: 50%">
				<label for="current_password">{$t('common.current_password')}</label>
				<input id="current_password" name="current_password" type="password">
			</div>
			<div style="width: 50%">
				<label for="new_password">{$t('common.new_password')}</label>
				<input id="new_password" minlength="8" name="new_password" type="password">
			</div>
		</div>
		<div class="row ver-center" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
</div>