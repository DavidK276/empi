<script lang="ts">
	import { t } from '$lib/translations';
	import { col, row } from '$lib/style.css';
	import { page } from '$app/stores';
	import { vars } from '$lib/theme.css';

	let user = $page.data.user;
	let participant = $page.data.participant;
</script>
<div class="{row} ver-center">
	<h1>{$t('account.my_account')}</h1>
	{#if user?.is_staff}
		<button style="background-color: {vars.danger}">Superuser</button>
	{:else}
		<button>Participant</button>
	{/if}
</div>
<h2>{$t('account.personal_info')}</h2>
<div class="{col}">
	{#if participant != null}
		<div class="{col}">
		<label for="token" title="{$t('common.token_hint')}">Token&nbsp;
			<span class="material-symbols-outlined">help</span>
		</label>
		<button id="token" style="font-size: 18px">{participant.token}</button>
	</div>
	{/if}
	<div class="{row}">
		<div style="width: 50%">
			<label for="first_name">{$t('common.first_name')}</label>
			<input type="text" id="first_name" readonly value="{user?.first_name}">
		</div>
		<div style="width: 50%">
			<label for="last_name">{$t('common.last_name')}</label>
			<input type="text" id="last_name" readonly value="{user?.last_name}">
		</div>
	</div>
	<div class="{row}">
		<div style="width: 50%">
			<label for="username">{$t('common.username')}</label>
			<input type="text" id="username" readonly value="{user?.username}">
		</div>
		<div style="width: 50%">
			<label for="email">Email</label>
			<input type="email" id="email" readonly value="{user?.email}">
		</div>
	</div>
</div>