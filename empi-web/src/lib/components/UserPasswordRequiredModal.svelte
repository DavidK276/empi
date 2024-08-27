<script lang="ts">
	import { t } from '$lib/translations';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { base } from "$app/paths";

	let password_ok: boolean | null = null;
	let modal: Modal;

	$: session = $page.data.session;
</script>

<svelte:component this={Modal} bind:this={modal} show="{!session?.user_password}" dismissible={false}>
	<div slot="header">
		<h2>{$t('common.password_entry_title')}</h2>
		<p>{$t('common.password_entry_text')}</p>
	</div>
	<form method="POST" action="{base}/?/checkPassword" use:enhance={() => {
		password_ok = null;
		return async ({result}) => {
			password_ok = result.type === 'success';
			if (password_ok) {
				modal.dismiss();
			}
		};
	}}>
		<label for="password">{$t('common.password')}</label>
		<input type="password" name="password" id="password">
		<button type="submit">{$t('common.check')}</button>
		{#if password_ok === false}
			<span style="color: var(--danger)">{$t('common.wrong_login')}</span>
		{/if}
	</form>
</svelte:component>