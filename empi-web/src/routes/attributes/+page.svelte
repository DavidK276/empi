<script lang="ts">
	import { t } from '$lib/translations';

	import type { PageData } from './$types';
	import Attribute from './Attribute.svelte';

	export let data: PageData;

	function addAttr(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Attribute({target: parent!, anchor: target});
	}
</script>
<h1>{$t('common.attributes')}</h1>
{#each data.attrs as attr}
	<Attribute {attr}></Attribute>
	<button on:click={addAttr}>{$t('attrs.add')}</button>
{:else}
	<p>{$t('attrs.no_attrs')}</p>
{/each}