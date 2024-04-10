<script lang="ts">
	import { t } from '$lib/translations';
	import { box, row } from '$lib/style.css';

	import type { PageData } from './$types';
	import type { Attribute } from '$lib/objects/attribute';
	import { vars } from '$lib/theme.css';
	import Option from './Option.svelte';

	export let data: PageData;

	const attrs: Attribute[] = data.attrs;

	function addOption(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Option({target: parent!, anchor: target, props: {value: null}});
	}
</script>
<h1>{$t('common.attributes')}</h1>
{#each attrs as attr}
	<div class="{box}">
		<form method="POST">
			<label for="name" style="margin: 0">{$t('attrs.name')}</label>
			<input type="text" name="name" id="name" value="{attr.name}" required>
			<label for="type">{$t('attrs.type')}</label>
			<select name="type" id="type">
				<option value="SC">{$t('attrs.single_choice')}</option>
				<option value="MC">{$t('attrs.multiple_choice')}</option>
				<option value="ET">{$t('attrs.enter_text')}</option>
			</select>
			{#if attr?.type !== 'EC'}
				<fieldset id="options">
					<legend>{$t('attrs.options')}</legend>
					{#each attr.values as value}
						<Option {value}></Option>
					{/each}
					<button type="button" style="margin-top: {vars.sm}" on:click={addOption}>+</button>
				</fieldset>
			{/if}
			<input type="hidden" name="url" value="{attr.url}">
			<button type="submit">{$t('common.submit')}</button>
		</form>
	</div>
{:else}
	<p>{$t('attrs.no_attrs')}</p>
{/each}