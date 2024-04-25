<script lang="ts">
	import { t } from '$lib/translations.js';
	import { store } from '$lib/stores.js';
	import { vars } from '$lib/theme.css.js';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';

	let password_ok: boolean | null = null;
	let modal: Modal;
</script>

<svelte:component this={Modal} bind:this={modal} show="{$store.password === ''}" dismissible={false}>
	<div slot="header">
		<h2>{$t('common.password_entry_title')}</h2>
		<p>{$t('common.password_entry_text')}</p>
	</div>
	<form method="POST" action="/?/checkPassword" use:enhance={() => {
		password_ok = null;
		return async ({result, formData}) => {
			password_ok = result.type === 'success';
			if (password_ok) {
				const password = formData.get('current_password');
				if (password != null) {
					$store.password = password.toString();
					modal.dismiss();
				}
			}
		};
	}}>
		<label for="password">{$t('common.password')}</label>
		<input type="password" name="current_password" id="password">
		<button type="submit">{$t('common.check')}</button>
		{#if password_ok === false}
			<span style="color: {vars.danger}">{$t('common.wrong_login')}</span>
		{/if}
	</form>
</svelte:component>