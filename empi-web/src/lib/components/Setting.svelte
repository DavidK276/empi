<script lang="ts">
	import { t } from '$lib/translations';
	import type { Attribute } from '$lib/objects/attribute';
	import { box } from '$lib/style.css';

	export let attr: Attribute;
	export let values: string[] = [];
</script>
<div class={box}>
	<h2 style="margin: var(--sm) 0">{attr.name}</h2>
	<fieldset id="options">
		<legend>{$t('attrs.options')}</legend>
		{#if attr.type === 'SC'}
			{#each attr.values as value}
				{#if values.includes(value)}
					<input type="radio" {value} id="{attr.name}_{value}" name="{attr.name}[]" checked>
				{:else}
					<input type="radio" {value} id="{attr.name}_{value}" name="{attr.name}[]">
				{/if}
				<label for="{attr.name}_{value}">{value}</label>
			{/each}
		{:else if attr.type === 'MC'}
			{#each attr.values as value}
				{#if values.includes(value)}
					<input type="checkbox" {value} id="{attr.name}_{value}" name="{attr.name}[]" checked>
				{:else}
					<input type="checkbox" {value} id="{attr.name}_{value}" name="{attr.name}[]">
				{/if}
				<label for="{attr.name}_{value}">{value}</label>
			{/each}
		{/if}
	</fieldset>
	<input type="hidden" name={attr.name} value="__blank__">
</div>

<style>
	label {
			display: inline;
	}
</style>