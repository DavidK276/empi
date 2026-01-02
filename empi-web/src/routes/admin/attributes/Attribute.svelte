<script lang="ts">

	import Option from './Option.svelte';

	import type { Attribute } from '$lib/objects/attribute';
	import { t } from '$lib/translations';
	import { ALLOW_TEXTENTRY_ATTR } from '$lib/constants';
	import { mount } from "svelte";

	function addOption(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		mount(Option, { target: parent!, anchor: target, props: { value: null } });
	}

	let { attr = null }: { attr?: Attribute | null } = $props();
	let chosen_type: string = $state("SC");
</script>
{#if attr != null}
	<div class="box">
		<form method="POST" action="?/admin">
			<label for="name">{$t('attrs.name')}</label>
			<input type="text" name="name" id="name" value={attr.name} required>
			<label for="type">{$t('attrs.type')}</label>
			<select name="type" id="type" disabled>
				<option value="SC" selected="{attr.type === 'SC'}">{$t('attrs.single_choice')}</option>
				<option value="MC" selected="{attr.type === 'MC'}">{$t('attrs.multiple_choice')}</option>
				{#if ALLOW_TEXTENTRY_ATTR}
					<option value="ET" selected="{attr.type === 'ET'}">{$t('attrs.enter_text')}</option>
				{/if}
			</select>
			{#if attr.type !== 'ET'}
				<fieldset id="options">
					<legend>{$t('attrs.options')}</legend>
					{#each attr.values as value(value)}
						<Option {value}></Option>
					{/each}
					<button type="button" onclick={addOption}>+</button>
				</fieldset>
			{/if}
			<input type="hidden" name="url" value={attr.url}>
			<button type="submit">{$t('common.submit')}</button>
			<button type="submit" name="delete" style="background-color: var(--danger)">{$t('attrs.delete')}</button>
		</form>
	</div>
{:else}
	<div class="box">
		<form method="POST" action="?/admin">
			<label for="name">{$t('attrs.name')}</label>
			<input type="text" name="name" id="name" required>
			<label for="type">{$t('attrs.type')}</label>
			<select name="type" id="type" bind:value={chosen_type}>
				<option value="SC">{$t('attrs.single_choice')}</option>
				<option value="MC">{$t('attrs.multiple_choice')}</option>
				{#if ALLOW_TEXTENTRY_ATTR}
					<option value="ET">{$t('attrs.enter_text')}</option>
				{/if}
			</select>
			{#if chosen_type !== 'ET'}
				<fieldset id="options">
					<legend>{$t('attrs.options')}</legend>
					<button type="button" style="margin-top: var(--sm)" onclick={addOption}>+</button>
				</fieldset>
			{/if}
			<input type="hidden" name="create">
			<button type="submit">{$t('common.submit')}</button>
		</form>
	</div>
{/if}
