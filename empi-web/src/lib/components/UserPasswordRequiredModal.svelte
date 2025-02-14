<script lang="ts">
	import { t } from '$lib/translations';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import { base } from "$app/paths";

	let session = page.data.session;

	let password_ok: boolean | null = $state(null);
	let show = $state(!session?.user_password);
</script>

<Modal bind:show={show} dismissible={false} hasCloseButton={false}>
	{#snippet header()}
		<h2>{$t('common.password_entry_title')}</h2>
		<p>{$t('common.password_entry_text')}</p>
	{/snippet}
	<form action="{base}/?/checkPassword" method="POST" use:enhance={() => {
		password_ok = null;
		return async ({result}) => {
			password_ok = result.type === 'success';
			if (password_ok) {
				show = false;
			}
		};
	}}>
		<label for="password">{$t('common.password')}</label>
		<input id="password" name="password" type="password">
		<button type="submit">{$t('common.check')}</button>
		{#if password_ok === false}
			<span style="color: var(--danger)">{$t('common.wrong_login')}</span>
		{/if}
	</form>
</Modal>