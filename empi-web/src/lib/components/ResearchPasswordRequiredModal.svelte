<script lang="ts">
	import { t } from '$lib/translations.js';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { onMount } from 'svelte';

	let password_ok: boolean | null = null;
	let modal: Modal;
	let show = false;

	onMount(async () => {
		const response = await fetch('?/checkPassword', { method: 'POST', body: new FormData() });
		const responseJSON = await response.json();
		show = responseJSON.type !== 'success';
	});
</script>

<svelte:component this={Modal} bind:this={modal} show={show} dismissible={false}>
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
		<div style="width: 100%">
			<button type="submit">{$t('common.check')}</button>
			{#if password_ok === false}
				<span style="color: var(--danger)">{$t('common.wrong_login')}</span>
			{/if}
		</div>
	</form>
</svelte:component>