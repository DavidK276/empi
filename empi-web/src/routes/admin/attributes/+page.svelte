<script lang="ts">
	import { t } from '$lib/translations';

	import type { PageData } from './$types';
	import Attribute from './Attribute.svelte';
	import Setting from '$lib/components/Setting.svelte';
	import { goto } from '$app/navigation';
	import { mount } from 'svelte';
	import { page } from '$app/state';
	import { enhance } from '$app/forms';
	import { resolve } from "$app/paths";

	let { data }: { data: PageData } = $props();

	let session = page.data.session;
	$effect(() => {
		if (!page.data.user.is_staff) {
			goto(resolve('/'), { replaceState: true });
		}
	});

	function addAttr(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		mount(Attribute, { target: parent!, anchor: target, props: {} });
	}

	let submitting = $state(false);
	let submit_success: boolean | null = $state(null);
</script>
<h1>{$t('common.attributes')}</h1>
{#if session?.user.is_staff === true}
	{#each data.attrs as attr}
		<Attribute {attr}></Attribute>
	{:else}
		<p>{$t('attrs.no_attrs')}</p>
	{/each}
	<button onclick={addAttr}>{$t('attrs.add')}</button>
{:else if session?.user.is_staff === false}
	<form method="POST"
	      action="?/user"
	      use:enhance={() => {
					submitting = true;
					submit_success = null;
					return async ({ update, result }) => {
						submit_success = result.type === "success";
						submitting = false;
						update({ reset: false });
					};
				}}>
		{#each data.attrs as attr}
			{#if Reflect.has(data.user_attrs, attr.name)}
				<Setting {attr} values={data.user_attrs[attr.name]}></Setting>
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
			<span style="margin: 0 var(--sm); color: var(--success)">{$t('attrs.success')}</span>
		{:else if submit_success === false}
			<span style="margin: 0 var(--sm); color: var(--danger)">{$t('common.unknown_error')}</span>
		{/if}
	</form>
{/if}
