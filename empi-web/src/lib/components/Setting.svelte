<script lang="ts">
	import { t } from '$lib/translations';
	import type { Attribute } from '$lib/objects/attribute';

	let { attr, values = [] }: { attr: Attribute, values?: string[] } = $props();
</script>
<div class="box">
	<h2 style="margin: var(--sm) 0">{attr.name}</h2>
	<fieldset id="options">
		<legend>{$t('attrs.options')}</legend>
		{#if attr.type === 'SC'}
			{#each attr.values as value(value)}
				{#if values.includes(value)}
					<input type="radio" {value} id="{attr.name}_{value}" name="{attr.name}[]" checked>
				{:else}
					<input type="radio" {value} id="{attr.name}_{value}" name="{attr.name}[]">
				{/if}
				<label for="{attr.name}_{value}">{value}</label>
			{/each}
		{:else if attr.type === 'MC'}
			{#each attr.values as value(value)}
				{#if values.includes(value)}
					<input type="checkbox" {value} id="{attr.name}_{value}" name="{attr.name}[]" checked>
				{:else}
					<input type="checkbox" {value} id="{attr.name}_{value}" name="{attr.name}[]">
				{/if}
				<label for="{attr.name}_{value}">{value}</label>
			{/each}
		{/if}
	</fieldset>
	<input name={attr.name} type="hidden" value="__blank__">
</div>

<style>
    label {
        display: inline;
    }
</style>
