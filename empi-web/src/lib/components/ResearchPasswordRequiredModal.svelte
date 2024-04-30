<script lang="ts">
	import { t } from '$lib/translations.js';
	import { vars } from '$lib/theme.css.js';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { invalidateAll } from '$app/navigation';

	let password_ok: boolean | null = null;
	let modal: Modal;

	$: session = $page.data.session;

	if (session?.research_password) {
		const formData = new FormData();
		formData.set('current_password', session.research_password);
		const href = new URL(document.location.href);
		fetch(href.origin + href.pathname + '/?/checkPassword', { method: 'POST', body: formData });
	}
</script>

<svelte:component this={Modal} bind:this={modal} show={!session?.research_password} dismissible={false}>
	<div slot="header">
		<h2>{$t('common.password_entry_title')}</h2>
		<p>{$t('common.password_entry_text')}</p>
	</div>
	<form method="POST" action="?/checkPassword"
				use:enhance={() => {
					password_ok = null;
					return async ({result}) => {
						password_ok = result.type === 'success';
						if (password_ok) {
							modal.dismiss()
							await invalidateAll();
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