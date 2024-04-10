<script lang="ts">

	import Option from './Option.svelte';
	import type { Attribute } from '$lib/objects/attribute';
	import { box } from '$lib/style.css';
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';

	function addOption(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Option({ target: parent!, anchor: target, props: { value: null } });
	}

	export let attr: Attribute | null = null;
</script>
{#if attr != null}
	<div class="{box}">
	<form method="POST">
		<label for="name" style="margin: 0">{$t('attrs.name')}</label>
		<input type="text" name="name" id="name" value="{attr.name}" required>
		<label for="type">{$t('attrs.type')}</label>
		<select name="type" id="type" disabled>
			<option value="SC" selected="{attr.type === 'SC'}">{$t('attrs.single_choice')}</option>
			<option value="MC" selected="{attr.type === 'MC'}">{$t('attrs.multiple_choice')}</option>
			<option value="ET" selected="{attr.type === 'ET'}">{$t('attrs.enter_text')}</option>
		</select>
		{#if attr.type !== 'EC'}
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
		<button type="submit" name="delete" style="background-color: {vars.danger}">{$t('attrs.delete')}</button>
	</form>
</div>
{:else}
	<div class="{box}">
	<form method="POST">
		<label for="name" style="margin: 0">{$t('attrs.name')}</label>
		<input type="text" name="name" id="name" required>
		<label for="type">{$t('attrs.type')}</label>
		<select name="type" id="type">
			<option value="SC">{$t('attrs.single_choice')}</option>
			<option value="MC">{$t('attrs.multiple_choice')}</option>
			<option value="ET">{$t('attrs.enter_text')}</option>
		</select>
			<fieldset id="options">
				<legend>{$t('attrs.options')}</legend>
				<button type="button" style="margin-top: {vars.sm}" on:click={addOption}>+</button>
			</fieldset>
		<input type="hidden" name="create">
		<button type="submit">{$t('common.submit')}</button>
	</form>
</div>
{/if}
