<script lang="ts">
	import { t } from '$lib/translations';

	import type { PageData } from './$types';
	import Attribute from './Attribute.svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	export let data: PageData;

	onMount(() => {
		// @ts-expect-error TS thinks data.user is always undefined, when it in fact isn't
		if (!data.user?.is_staff) {
			goto('/', { replaceState: true });
		}
	});

	function addAttr(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Attribute({ target: parent!, anchor: target });
	}
</script>
<h1>{$t('common.attributes')}</h1>
{#each data.attrs as attr}
	<Attribute {attr}></Attribute>
{:else}
	<p>{$t('attrs.no_attrs')}</p>
{/each}
<button on:click={addAttr}>{$t('attrs.add')}</button>