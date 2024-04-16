<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';
	import Setting from '../../attributes/Setting.svelte';
	import { enhance } from '$app/forms';
	import { row } from '$lib/style.css';

	export let data: PageData;
	let submitting = false;
	let submit_success: boolean | null = null;
	console.log(data);
</script>
<div class="{row} ver-center">
	<h1>{data.research.name}</h1>
	{#if data.research?.is_published === false}
		<button style="height: 100%; background-color: {vars.danger}">{$t('research.unpublished')}</button>
		<form method="POST" action="?/publish" use:enhance>
			<button type="submit">{$t('research.publish')}<span class="material-symbols-outlined">visibility</span></button>
		</form>
	{:else if data.research?.is_published === true}
		<button>{$t('research.published')}</button>
		<form method="POST" action="?/unpublish" use:enhance>
			<button type="submit" style="background-color: {vars.danger}">{$t('research.unpublish')}<span class="material-symbols-outlined">visibility_off</span></button>
		</form>
	{/if}
</div>
<label for="url">{$t('research.info_url')}</label>
<input type="text" id="url" readonly value="{data.research.info_url}">
<form method="POST"
			action="?/attrs"
			use:enhance={() => {
					submitting = true;
					submit_success = null;
					return async ({ update, result }) => {
						submit_success = false;
						if (result.status != null)
							submit_success = 200 <= result.status && result.status <= 399;
						submitting = false;
						update({ reset: false });
					};
				}}>
	{#each data.attrs as attr}
		{#if Reflect.has(data.research_attrs, attr.name)}
			<Setting {attr} values="{data.research_attrs[attr.name]}"></Setting>
		{:else}
			<Setting {attr}></Setting>
		{/if}
	{:else}
		<p>{$t('attrs.no_attrs')}</p>
	{/each}
	{#if submitting}
		<button type="submit" style="margin-top: 0" disabled>{$t('common.submitting')}</button>
	{:else}
		<button type="submit" style="margin-top: 0">{$t('common.submit')}</button>
	{/if}
	{#if submit_success === true}
		<span style="margin: 0 {vars.sm}; color: green">{$t('attrs.success')}</span>
	{:else if submit_success === false}
		<span style="margin: 0 {vars.sm}; color: {vars.danger}">{$t('common.unknown_error')}</span>
	{/if}
</form>