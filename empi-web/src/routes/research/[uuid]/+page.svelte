<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';
	import Setting from '$lib/components/Setting.svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import {
		accordion,
		accordionTab,
		accordionTabContent,
		accordionTabInput,
		accordionTabLabel,
		row
	} from '$lib/style.css';
	import Appointment from './Appointment.svelte';
	import { Appointment as Appt } from '$lib/objects/appointment';
	import { convertFormData } from '$lib/functions';
	import { plainToInstance } from 'class-transformer';

	export let data: PageData;
	let appointments = plainToInstance(Appt, data.appointments);
	let submitting_attrs = false;
	let submit_success_attrs: boolean | null = null;
	let submitting_appointments = false;
	let submit_success_appointments: boolean | null = null;

	function addAppointment(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Appointment({ target: parent!, anchor: target, props: { uuid: $page.params.uuid } });
	}

	async function submitAppointments() {
		const forms = document.getElementsByClassName('appointment-form');
		const appointments: Appt[] = [];
		for (const element of forms) {
			const form = element as HTMLFormElement;
			const formData = new FormData(form);
			const appointment: Appt = convertFormData({ formData, stringify: false });
			appointments.push(appointment);
		}

		submitting_appointments = true;
		const response = await fetch('?/appointments', {
			body: JSON.stringify(appointments),
			method: 'POST'
		});
		submitting_appointments = false;
		submit_success_appointments = response.ok;
	}
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
			<button type="submit" style="background-color: {vars.danger}">{$t('research.unpublish')}<span
				class="material-symbols-outlined">visibility_off</span></button>
		</form>
	{/if}
</div>
<label for="url">{$t('research.info_url')}</label>
<input type="text" id="url" readonly value="{data.research.info_url}">
<div class="{accordion}">
	<div class="{accordionTab}">
		<input type="checkbox" name="research-accordion" id="cb1" class="{accordionTabInput}" checked>
		<label for="cb1" class="{accordionTabLabel}">{$t('common.attributes')}
			<span class="material-symbols-outlined">expand_more</span>
		</label>
		<div class="{accordionTabContent}">
			<form method="POST"
						action="?/attrs"
						use:enhance={() => {
							submitting_attrs = true;
							submit_success_attrs = null;
							return async ({ update, result }) => {
								submit_success_attrs = false;
								if (result.status != null)
									submit_success_attrs = 200 <= result.status && result.status <= 399;
								submitting_attrs = false;
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
				{#if submitting_attrs}
					<button type="submit" style="margin-top: 0" disabled>{$t('common.submitting')}</button>
				{:else}
					<button type="submit" style="margin-top: 0">{$t('common.submit')}</button>
				{/if}
				{#if submit_success_attrs === true}
					<span style="margin: 0 {vars.sm}; color: green">{$t('attrs.success')}</span>
				{:else if submit_success_attrs === false}
					<span style="margin: 0 {vars.sm}; color: {vars.danger}">{$t('common.unknown_error')}</span>
				{/if}
			</form>
		</div>
	</div>
	<div class="{accordionTab}">
		<input type="checkbox" name="research-accordion" id="cb2" class="{accordionTabInput}" checked>
		<label for="cb2" class="{accordionTabLabel}">{$t('research.appointments')}
			<span class="material-symbols-outlined">expand_more</span>
		</label>
		<div class="{accordionTabContent}">
			{#each appointments as appointment}
				<Appointment {appointment} uuid="{$page.params.uuid}"></Appointment>
			{/each}
			<button type="button" on:click={addAppointment}>+</button>
			{#if submitting_appointments}
				<button type="submit" disabled>{$t('common.submitting')}</button>
			{:else}
				<button type="submit" on:click={submitAppointments}>{$t('common.submit')}</button>
			{/if}
			{#if submit_success_appointments === true}
				<span style="margin: 0 {vars.sm}; color: green">{$t('attrs.success')}</span>
			{:else if submit_success_appointments === false}
				<span style="margin: 0 {vars.sm}; color: {vars.danger}">{$t('common.unknown_error')}</span>
			{/if}
		</div>
	</div>
</div>