<script lang="ts">
	import type { PageServerData } from './$types';
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';
	import Setting from '$lib/components/Setting.svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { box, col, error, row } from '$lib/style.css';
	import Appointment from './Appointment.svelte';
	import { Appointment as Appt } from '$lib/objects/appointment';
	import { convertFormData } from '$lib/functions';
	import { plainToInstance } from 'class-transformer';
	import Accordion from '$lib/components/Accordion.svelte';
	import AccordionTab from '$lib/components/AccordionTab.svelte';
	import { Participation } from '$lib/objects/participation';
	import EmailInput from '$lib/components/EmailInput.svelte';
	import { invalidateAll } from '$app/navigation';
	import FormResultMessage from '$lib/components/FormResultMessage.svelte';
	import ResearchPasswordRequiredModal from '$lib/components/ResearchPasswordRequiredModal.svelte';

	export let data: PageServerData;
	$: appointments = plainToInstance(Appt, data.appointments);
	let emails: EmailInput;
	let submitting_attrs = false;
	let submit_success_attrs: boolean | null = null;
	let submitting_appointments = false;
	let submit_success_appointments: boolean | null = null;
	let submitting_participations = false;
	let submit_success_participations: boolean | null = null;

	function addAppointment(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		new Appointment({ target: parent!, anchor: target, props: { nanoid: $page.params.nanoid } });
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

	async function submitParticipations() {
		const forms = document.getElementsByClassName('participation-form');
		const participations: Participation[] = [];
		for (const element of forms) {
			const form = element as HTMLFormElement;
			const formData = new FormData(form);
			const participation: Participation = convertFormData({ formData, stringify: false });
			participations.push(participation);
		}

		submitting_participations = true;
		const response = await fetch('?/participations', {
			body: JSON.stringify(participations),
			method: 'POST'
		});
		submitting_participations = false;
		submit_success_participations = response.ok;
	}
</script>
<ResearchPasswordRequiredModal></ResearchPasswordRequiredModal>
{#if data.research != null}
	<div class="{row} ver-center m-col" style="margin-bottom: {vars.sm}">
		<h1 style="margin: {vars.sm} 0">{data.research.name}</h1>
		{#if data.research?.is_published === false}
			<button style="height: 100%; background-color: {vars.danger}">{$t('research.unpublished')}</button>
			<form method="POST" action="?/publish" use:enhance>
				<button type="submit">{$t('research.publish')}<span class="material-symbols-outlined">visibility</span></button>
			</form>
		{:else if data.research?.is_published === true}
			<button style="background: {vars.success}">{$t('research.published')}</button>
			<form method="POST" action="?/unpublish" use:enhance>
				<button type="submit" style="background-color: {vars.danger}">{$t('research.unpublish')}<span
					class="material-symbols-outlined">visibility_off</span></button>
			</form>
		{/if}
	</div>
	<form method="POST" action="?/update"
				on:formdata={(event) => event.formData.set('email_recipients', emails.getEmails())}>
		<label for="url">{$t('research.info_url')}</label>
		<input type="text" id="url" name="info_url" value={data.research.info_url}>
		<EmailInput bind:this={emails} emails={data.research.email_recipients}></EmailInput>
		<button type="submit" style="margin-bottom: {vars.lg}">{$t('common.submit')}</button>
	</form>
	<Accordion>
		<AccordionTab id="cb0" checked={!data.research.is_protected} title={$t('research.protection')}>
			<form method="POST" action="?/setPassword"
						use:enhance={({submitter}) => {
							if (submitter != null) {
								submitter.toggleAttribute('disabled');
								submitter.innerHTML = $t('common.submitting');
							}

							return async ({formElement, result, update}) => {
								await invalidateAll();
								await update();
								if (submitter != null) {
									submitter.toggleAttribute('disabled');
									submitter.innerHTML = $t('common.submit');

									const submitDiv = formElement.children.namedItem('submit-div');
									if (submitDiv != null) {
										new FormResultMessage({target: submitDiv, props: {type: result.type}});
									}
								}
							};
					}}>
				{#if !data.research.is_protected}
					<p class="{error}" style="display: flex"><span
						class="material-symbols-outlined">warning</span>&nbsp;{$t('research.unprotected_warning')}</p>
					<input type="hidden" name="current_password" value="__blank__">
				{:else}
					<label for="current_password">{$t('common.current_password')}</label>
					<input type="password" name="current_password" id="current_password">
				{/if}
				<label for="new_password">{$t('common.new_password')}</label>
				<input type="password" name="new_password" id="new_password">
				<div class="{row} ver-center" id="submit-div">
					<button type="submit" id="submit">{$t('common.submit')}</button>
				</div>
			</form>
		</AccordionTab>
		<AccordionTab id="cb1" checked={false} title={$t('common.attributes')}>
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
						<Setting {attr} values={data.research_attrs[attr.name]}></Setting>
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
		</AccordionTab>
		<AccordionTab id="cb2" checked={false} title={$t('research.appointments')}>
			{#each appointments as appointment}
				<Appointment {appointment} nanoid={$page.params.nanoid}></Appointment>
			{/each}
			<button type="button" on:click={addAppointment}>+</button>
			{#if submitting_appointments}
				<button type="button" disabled>{$t('common.submitting')}</button>
			{:else}
				<button type="button" on:click={submitAppointments}>{$t('common.submit')}</button>
			{/if}
			{#if submit_success_appointments === true}
				<span style="margin: 0 {vars.sm}; color: green">{$t('attrs.success')}</span>
			{:else if submit_success_appointments === false}
				<span style="margin: 0 {vars.sm}; color: {vars.danger}">{$t('common.unknown_error')}</span>
			{/if}
		</AccordionTab>
		<AccordionTab id="cb3" checked={data.participations?.length > 0} title={$t('research.protocol')}>
			<div class={col}>
				{#if data.participations}
					{#each data.participations as p_row}
						{@const width = 100 / p_row.length}
						<div class="{row} m-col">
							{#each p_row as participation}
								<div class={box} style="min-width: {width}%">
									<form style="display: flex; justify-content: center;" class="participation-form">
										<button style="font-weight: 700; text-align: center">{participation.token}</button>
										<input type="hidden" name="id" value={participation.id}>
										{#if participation.has_participated}
											<input type="checkbox" name="has_participated" checked style="margin: 0 {vars.sm}" value="true">
										{:else}
											<input type="checkbox" name="has_participated" style="margin: 0 {vars.sm}" value="true">
										{/if}
									</form>
								</div>
							{/each}
						</div>
					{/each}
				{:else}
					<p>{$t('research.no_participations')}</p>
				{/if}
			</div>
			{#if data.participations && data.participations.length > 0}
				{#if submitting_participations}
					<button type="button" disabled>{$t('common.submitting')}</button>
				{:else}
					<button type="button" on:click={submitParticipations}>{$t('common.submit')}</button>
				{/if}
				{#if submit_success_participations === true}
					<span style="margin: 0 {vars.sm}; color: green">{$t('attrs.success')}</span>
				{:else if submit_success_participations === false}
					<span style="margin: 0 {vars.sm}; color: {vars.danger}">{$t('common.unknown_error')}</span>
				{/if}
			{/if}
		</AccordionTab>
	</Accordion>
{/if}