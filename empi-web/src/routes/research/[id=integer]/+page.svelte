<script lang="ts">
	import type { ActionData, PageData } from './$types';
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import { store } from '$lib/stores';
	import { page } from '$app/stores';
	import { type Writable, writable } from 'svelte/store';
	import type { Participation } from '$lib/objects/participation';
	import { onMount } from 'svelte';
	import { goto, invalidateAll } from '$app/navigation';
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import { localeDateStringFromUTCString } from "$lib/functions";

	export let data: PageData;
	export let form: ActionData;

	store.subscribe(() => getSignups());

	async function getSignups() {
		if (!$store.user_password || $page.data.user.is_staff) {
			return;
		}
		const formData = new FormData();
		formData.set('current_password', $store.user_password);
		const response = await fetch('/server/participations/user', { method: 'POST', body: formData });
		const responseJSON = await response.json() as Array<{
			appointment: number,
			is_confirmed: boolean,
			research: number
		}>;
		const participationMap = new Map();
		for (const participation of responseJSON) {
			if (participation.research === data.research?.id) {
				participationMap.set(participation.appointment, participation);
				can_signup = false;
				is_confirmed ||= participation.is_confirmed;
			}
		}
		participations.set(participationMap);
	}

	async function cancelSignup(event: Event) {
		const form = event.target as HTMLFormElement;
		const formData = new FormData(form);
		formData.set('current_password', $store.user_password);
		const participationId = formData.get('participation')!;
		formData.delete('participation');

		await fetch(`/server/participations/${participationId}/`, { method: 'DELETE', body: formData });

		await invalidateAll();
		await getSignups();
		can_signup = true;
		is_confirmed = false;
	}

	onMount(() => {
		if (form?.success && form.participation != null) {
			goto(`/participation/${form.participation.nanoid}/`);
		}
	});

	let participations: Writable<Map<number, Participation>> = writable();
	let can_signup = !$page.data.user?.is_staff;
	let is_confirmed = false;
</script>
{#if $page.data.user != null}
	<UserPasswordRequiredModal></UserPasswordRequiredModal>
{/if}
<div class="row m-col">
	<h1 style="display: inline; margin: 0">{data.research?.name}</h1>
	{#if is_confirmed}
		<p class="message">
			<MaterialSymbolsInfoOutline width="24"
			                            height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.participated')}</p>
	{/if}
</div>
<p>{$t('research.info_url_introduction')} <a href={data.research?.info_url} target="_blank">{$t('research.here')}</a>
</p>
{#each data.appointments as appointment, i}
	{@const participation = $participations?.get(appointment.id)}
	{@const is_signedup = participation?.is_confirmed === false}
	<div class="box">
		<div class="row ver-center">
			<h2>{$t('research.appointment_number')} {i + 1}</h2>
			{#if appointment.location}
				<button>{$t('research.in_person')}</button>
			{:else}
				<button>{$t('research.online')}</button>
			{/if}
			{#if is_signedup}
				<button style="background: var(--success)">{$t('research.appointment_signedup')}</button>
			{/if}
		</div>
		<p>{appointment.comment}</p>
		<div style="width: 50%" class="m-w-full">
			<table style="width: 100%; margin-bottom: var(--sm)">
				<tr>
					<th>{$t('research.when')}</th>
					{#if appointment.location}
						<th>{$t('research.location')}</th>
					{:else if is_signedup}
						<th>{$t('research.join_appointment_url')}</th>
					{/if}
					<th>{$t('research.capacity')}</th>
				</tr>
				<tr>
					<td>
						<time datetime="{appointment.when}">{localeDateStringFromUTCString(appointment.when)}</time>
					</td>
					{#if appointment.location}
						<td>{appointment.location}</td>
					{:else if is_signedup}
						<td><a href={appointment.info_url} target="_blank">{$t('research.join_appointment')}</a></td>
					{/if}
					<td style="text-align: center">
						<span style="color: {appointment.free_capacity ? 'initial' : 'red'}">{appointment.free_capacity}</span>
					</td>
				</tr>
			</table>
			{#if can_signup && appointment.free_capacity}
				<form method="POST" action="?/signup">
					<input type="hidden" name="appointment" value={appointment.id}>
					{#if $page.data.user == null}
						<label for="recipient">Email</label>
						<input type="email" name="recipient" id="recipient" class="m-w-full">
					{/if}
					<div class="row ver-center">
						<button type="submit">{$t('research.signup')}</button>
						{#if $page.data.user == null}
							<p class="message">
								<MaterialSymbolsInfoOutline width="24" height="24"
								></MaterialSymbolsInfoOutline>&nbsp;{$t('research.anonymous_signup')}
							</p>
						{/if}
					</div>
				</form>
			{/if}
			{#if is_signedup}
				<form method="POST" on:submit|preventDefault={cancelSignup}>
					<input type="hidden" name="participation" value={participation?.id}>
					<button type="submit" style="background: var(--danger)">{$t('research.cancel')}</button>
				</form>
			{/if}
		</div>
	</div>
{:else}
	<p class="message">
		<MaterialSymbolsInfoOutline width="24"
		                            height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.no_appointments')}</p>
{/each}