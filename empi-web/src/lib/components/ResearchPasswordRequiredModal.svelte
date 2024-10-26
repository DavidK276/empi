<script lang="ts">
	import { t } from '$lib/translations';
	import Modal from '$lib/components/Modal.svelte';
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { onMount } from 'svelte';

	let password_ok: boolean | null = $state(null);
	let modal;
	let show = $state(false);

	onMount(async () => {
		const response = await fetch('?/checkPassword', { method: 'POST', body: new FormData() });
		const responseJSON = await response.json();
		show = responseJSON.type !== 'success';
	});
</script>

<Modal bind:this={modal} dismissible={false} hasCloseButton={false} show={show}>
	{#snippet header()}
		<h2>{$t('common.password_entry_title')}</h2>
		<p>{$t('common.password_entry_text')}</p>
	{/snippet}
	<form action="?/checkPassword" method="POST"
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
		<input id="password" name="password" type="password">
		<div style="width: 100%">
			<button type="submit">{$t('common.check')}</button>
			{#if password_ok === false}
				<span style="color: var(--danger)">{$t('common.wrong_login')}</span>
			{/if}
		</div>
	</form>
</Modal>