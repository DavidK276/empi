<script lang="ts">
	import type { PageServerData } from './$types';
	import { t } from '$lib/translations';
	import Setting from '$lib/components/Setting.svelte';
	import { enhance } from '$app/forms';
	import { universalEnhance } from '$lib/enhanceFunctions';
	import { page } from '$app/state';
	import Appointment from './Appointment.svelte';
	import { Appointment as Appt } from '$lib/objects/appointment';
	import { convertFormData, localeDateStringFromUTCString, textAreaAdjustSize } from '$lib/functions';
	import { plainToInstance } from 'class-transformer';
	import Accordion from '$lib/components/Accordion.svelte';
	import AccordionTab from '$lib/components/AccordionTab.svelte';
	import EmailInput from '$lib/components/EmailInput.svelte';
	import ResearchPasswordRequiredModal from '$lib/components/ResearchPasswordRequiredModal.svelte';
	import MaterialSymbolsWarningOutline from 'virtual:icons/material-symbols/warning-outline';
	import MaterialSymbolsVisibilityOutline from 'virtual:icons/material-symbols/visibility-outline';
	import MaterialSymbolsVisibilityOffOutline from 'virtual:icons/material-symbols/visibility-outline';
	import { ENABLE_ATTRS, TOKEN_REGEX } from '$lib/constants';
	import MarkdownGuideModal from "$lib/components/MarkdownGuideModal.svelte";
	import { mount, onMount } from "svelte";
	import { goto, invalidateAll } from "$app/navigation";
	import { resolve } from "$app/paths";
	import Participations from "$lib/components/Participations.svelte";
	import type { IParticipation } from "$lib/objects/participation";
	import FormResultMessage from "$lib/components/FormResultMessage.svelte";

	let { data }: { data: PageServerData } = $props();

	let appointments = $derived(plainToInstance(Appt, data.appointments));
	let emails = $state<EmailInput>(null!);
	let submitting_appointments = $state(false);
	let submit_success_appointments: boolean | null = $state(null);
	let submitting_participations = $state(false);
	let submit_success_participations: boolean | null = $state(null);
	let showMarkdownGuide = $state(false);

	function addAppointment(e: Event) {
		const target = e.target as HTMLButtonElement;
		const parent = target.parentElement;
		mount(Appointment, { target: parent!, anchor: target, props: { nanoid: page.params.nanoid! } });
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
		submitting_participations = true;
		const forms = document.getElementsByClassName('participation-form');
		const participations: IParticipation[] = [];
		for (const element of forms) {
			const form = element as HTMLFormElement;
			const formData = new FormData(form);
			const participation = convertFormData({ formData, stringify: false });
			participations.push(participation);
		}

		const response = await fetch('?/participations', {
			body: JSON.stringify(participations),
			method: 'POST'
		});
		await invalidateAll();
		submitting_participations = false;
		submit_success_participations = response.ok;
	}

	async function setParticipationsFromCsv(e: MouseEvent) {
		const fileInput = document.getElementById('participationFileInput') as HTMLInputElement;
		const file: File | null | undefined = fileInput?.files?.item(0);
		if (file == null) {
			return;
		}
		const text = await file.text();
		const matches: Set<string> = new Set([...text.matchAll(TOKEN_REGEX)].map(a => a[0]));
		// eslint-disable-next-line svelte/prefer-svelte-reactivity
		const checkedTokens: Set<string> = new Set();
		// eslint-disable-next-line svelte/prefer-svelte-reactivity
		const uncheckedTokens: Set<string> = new Set();

		const keepExisting = (document.getElementById('keepExistingCheckbox') as HTMLInputElement).checked;
		if (!keepExisting) {
			for (let checkbox of document.getElementsByClassName('participation-checkbox') as Iterable<HTMLInputElement>) {
				if (checkbox.checked) {
					const tokenMatch = checkbox.id.match(TOKEN_REGEX);
					if (tokenMatch && !matches.has(tokenMatch[0])) {
						uncheckedTokens.add(tokenMatch[0]);
						checkbox.checked = false;
					}
				}
			}
		}

		matches.forEach(token => {
			const checkbox = document.getElementById(`participation-checkbox-${token}`) as HTMLInputElement | null;
			if (checkbox != null && !checkbox.checked) {
				checkbox.checked = true;
				checkedTokens.add(token);
				uncheckedTokens.delete(token);
			}
		});

		const submitButton = e.target as HTMLButtonElement;
		const message = `V dokumente sa našlo ${matches.size} identifikátorov. Bolo potvrdených ${checkedTokens.size} účastí a ${uncheckedTokens.size} účastí bolo zrušených.`;
		mount(FormResultMessage, { target: submitButton.parentElement!, anchor: submitButton, props: { message } });
	}

	onMount(() => {
		if (!page.data.user?.is_staff) {
			goto(resolve('/'), { replaceState: true });
		}
	});
</script>
<ResearchPasswordRequiredModal></ResearchPasswordRequiredModal>
<MarkdownGuideModal bind:show={showMarkdownGuide}></MarkdownGuideModal>
{#if data.research != null}
	<div class="row ver-center m-col" style="margin-bottom: var(--sm)">
		<h1 style="margin: var(--sm) 0">{data.research.name}</h1>
		{#if data.research?.is_published === false}
			<div class="row">
				<button style="height: 100%; background: var(--danger)"><span
					style="height: 24px; align-content: center">{$t('research.unpublished')}</span></button>
				<form method="POST" action="?/publish" use:enhance>
					<button type="submit">{$t('research.publish')}
						<MaterialSymbolsVisibilityOutline width="24" height="24"></MaterialSymbolsVisibilityOutline>
					</button>
				</form>
			</div>
		{:else if data.research?.is_published === true}
			<div class="row">
				<button style="background: var(--success)"><span
					style="height: 24px; align-content: center">{$t('research.published')}</span></button>
				<form method="POST" action="?/unpublish" use:enhance>
					<button type="submit" style="background: var(--danger)">{$t('research.unpublish')}
						<MaterialSymbolsVisibilityOffOutline width="24"
						                                     height="24"></MaterialSymbolsVisibilityOffOutline>
					</button>
				</form>
			</div>
		{/if}
	</div>
	<label for="page-url">{$t('research.page_url')}</label>
	<input type="url" id="page-url" readonly value="{page.url}">
	<form method="POST" action="?/update"
	      use:enhance={({formElement, submitter}) => {
					return universalEnhance({formElement, submitter}, {
						idleMessage: $t('common.submit'),
						runningMessage: $t('common.submitting'),
						reset: false,
						invalidateAll: true
					});
				}}
	      onformdata={(event) => event.formData.set('email_recipients', emails?.getEmails())}>
		<div class="row">
			<div style="width: 50%; display: inline-block" class="m-w-full">
				<label for="points">{$t('common.points')}</label>
				<input type="number" min="1" max="1000" id="points" name="points" value="{data.research.points}">
			</div>
			<div style="width: 50%; display: inline-block" class="m-w-full">
				<label for="url">{$t('research.info_url')}</label>
				<input type="url" id="url" name="info_url" maxlength="500" value={data.research.info_url}>
			</div>
		</div>
		<label for="comment">{$t('research.comment')}&nbsp;({$t('research.supports')}&nbsp;<a
			href="/" target="_blank"
			onclick={(e) => {e.preventDefault(); showMarkdownGuide = true}}>markdown</a>)</label>
		<textarea id="comment" name="comment" onkeyup={textAreaAdjustSize}
		          onclick={textAreaAdjustSize}>{data.research.comment}</textarea>
		<EmailInput bind:this={emails} emails={data.research.email_recipients}></EmailInput>
		<div class="row ver-center" style="margin-bottom: var(--lg)" id="submit-div">
			<button type="submit">{$t('common.submit')}</button>
		</div>
	</form>
	<Accordion>
		{#if data.research.is_protected}
			<AccordionTab open={false} title={$t('research.protection')}>
				<form method="POST" action="?/setPassword"
				      use:enhance={({formElement, submitter}) => {
							return universalEnhance({formElement, submitter}, {
								idleMessage: $t('common.submit'),
								runningMessage: $t('common.submitting'),
								reset: true,
								invalidateAll: true
							});
						}}>
					{#if !data.research.is_protected}
						<div class="error-msg row ver-center no-gap">
							<MaterialSymbolsWarningOutline width="24"
							                               height="24"></MaterialSymbolsWarningOutline>&nbsp;{$t('research.unprotected_warning')}
						</div>
						<input type="hidden" name="current_password" value="__blank__">
					{:else}
						<label for="current_password">{$t('common.current_password')}</label>
						<input type="password" name="current_password" id="current_password">
					{/if}
					<label for="new_password">{$t('common.new_password')}</label>
					<input type="password" name="new_password" id="new_password" required minlength="8">
					<div class="row ver-center" id="submit-div">
						<button type="submit" id="submit">{$t('common.submit')}</button>
					</div>
				</form>
			</AccordionTab>
		{/if}
		{#if ENABLE_ATTRS && data.attrs?.length > 0}
			<AccordionTab open={false} title={$t('common.attributes')}>
				<form method="POST" action="?/attrs"
				      use:enhance={({formElement, submitter}) => {
								return universalEnhance({formElement, submitter}, {
									idleMessage: $t('common.submit'),
									runningMessage: $t('common.submitting'),
									reset: false,
									invalidateAll: true
								});
							}}>
					{#each data.attrs as attr(attr.name)}
						{#if Reflect.has(data.research_attrs, attr.name)}
							<Setting {attr} values={data.research_attrs[attr.name]}></Setting>
						{:else}
							<Setting {attr}></Setting>
						{/if}
					{/each}
					<div class="row ver-center" id="submit-div">
						<button type="submit" id="submit">{$t('common.submit')}</button>
					</div>
				</form>
			</AccordionTab>
		{/if}
		<AccordionTab open={false} title={$t('research.appointments')}>
			{#each appointments as appointment (appointment.id)}
				<Appointment {appointment} nanoid={page.params.nanoid || ''}></Appointment>
			{/each}
			<button type="button" onclick={addAppointment}>+</button>
			{#if submitting_appointments}
				<button type="button" disabled>{$t('common.submitting')}</button>
			{:else}
				<button type="button" onclick={submitAppointments}>{$t('common.submit')}</button>
			{/if}
			{#if submit_success_appointments === true}
				<span style="margin: 0 var(--sm); color: var(--success)">{$t('attrs.success')}</span>
			{:else if submit_success_appointments === false}
				<span style="margin: 0 var(--sm); color: var(--danger)">{$t('common.unknown_error')}</span>
			{/if}
		</AccordionTab>
		<AccordionTab open={false} title={$t('research.send_email')}>
			<form method="POST" action="?/email"
			      use:enhance={({formElement, submitter}) => {
							return universalEnhance({formElement, submitter}, {
								idleMessage: $t('common.send'),
								runningMessage: $t('common.sending'),
								reset: true,
								invalidateAll: true
							});
						}}>
				<fieldset>
					<legend>Príjemcovia</legend>
					<label for="appointment">Používatelia prihlásení na termín</label>
					<select name="appointment" id="appointment">
						<option value="">žiadny</option>
						{#each appointments as appointment (appointment.id)}
							{#if appointment.info_url != null}
								<option value={appointment.id}>{localeDateStringFromUTCString(appointment.when)}
									, {$t('research.online').toLowerCase()}</option>
							{:else}
								<option value={appointment.id}>{localeDateStringFromUTCString(appointment.when)}
									, {$t('research.in_person').toLowerCase()}</option>
							{/if}
						{/each}
					</select>
					<label for="extra_recipients">Ďalší príjemcovia (oddelení čiarkou)</label>
					<input type="text" name="extra_recipients" id="extra_recipients">
				</fieldset>
				<label for="subject">Predmet&nbsp;({$t('common.optional')})</label>
				<input type="text" name="subject" id="subject" maxlength="78">
				<label for="body">Text emailu&nbsp;({$t('research.supports')}&nbsp;<a
					href="/" target="_blank"
					onclick={(e) => {e.preventDefault(); showMarkdownGuide = true}}>markdown</a>)</label>
				<textarea id="body" name="body" onkeyup={textAreaAdjustSize}></textarea>
				<div class="row ver-center" id="submit-div">
					<button type="submit" id="submit">{$t('common.send')}</button>
				</div>
			</form>
		</AccordionTab>
		{#await data.participations}
			<AccordionTab open={false} title={$t('research.protocol')}>
				<p>{$t('common.loading')}</p>
			</AccordionTab>
		{:then participations}
			{@const hasParticipations = participations.unconfirmed.length > 0 || participations.confirmed.length > 0}
			<AccordionTab open={hasParticipations} title={$t('research.protocol')}>
				<Participations {participations}></Participations>
				{#if hasParticipations}
					<form style="width: 33%">
						<fieldset>
							<legend>{$t('research.csv_import')}</legend>
							<input type="file" id="participationFileInput" accept="text/*">
							<label for="keepExistingCheckbox"
							       style="display: inline">{$t('research.keep_existing')}</label>
							<input type="checkbox" id="keepExistingCheckbox" checked>
							<div class="row hor-right" style="padding-top: var(--lg)">
								<button type="button" onclick={setParticipationsFromCsv}
								        style="cursor: pointer">{$t('common.insert')}</button>
							</div>
						</fieldset>
					</form>
					{#if submitting_participations}
						<button type="button" disabled>{$t('common.submitting')}</button>
					{:else}
						<button type="button" onclick={submitParticipations}>{$t('common.submit')}</button>
					{/if}
					{#if submit_success_participations === true}
						<span style="margin: 0 var(--sm); color: var(--success)">{$t('attrs.success')}</span>
					{:else if submit_success_participations === false}
						<span style="margin: 0 var(--sm); color: var(--danger)">{$t('common.unknown_error')}</span>
					{/if}
				{/if}
			</AccordionTab>
		{/await}
	</Accordion>
{/if}
