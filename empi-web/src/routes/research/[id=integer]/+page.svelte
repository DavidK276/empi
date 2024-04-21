<script lang="ts">
	import type { PageData } from './$types';
	import PasswordRequiredModal from '$lib/components/PasswordRequiredModal.svelte';
	import { box, row } from "$lib/style.css";
	import { t } from "$lib/translations";
	import { store } from "$lib/stores";
	import { type Writable, writable } from "svelte/store";
	import { vars } from "$lib/theme.css";

	export let data: PageData;

	store.subscribe(async ({ password }) => {
		if (!password) {
			return
		}
		const formData = new FormData();
		formData.set('current_password', password);
		const href = new URL(document.location.href);
		const url = href.origin + href.pathname;
		const response = await fetch(url, { method: 'POST', body: formData });
		const responseJSON = await response.json() as Array<{
			appointment: number,
			has_participated: boolean,
			research: number
		}>;
		const participationMap = new Map();
		for (const participation of responseJSON) {
			if (participation.research === data.research?.id) {
				participationMap.set(participation.appointment, participation.has_participated);
				can_signup = false;
				has_participated ||= participation.has_participated;
			}
		}
		participations.set(participationMap);
	});
	let participations: Writable<Map<number, boolean>> = writable();
	let can_signup = true;
	let has_participated = false;
</script>
<PasswordRequiredModal></PasswordRequiredModal>
<div class="{row} m-col">
	<h1 style="display: inline; margin: 0">{data.research?.name}</h1>
	{#if has_participated}
		<span style="display: inline-flex; align-items: center"><span
				class="material-symbols-outlined">info</span>&nbsp{$t('research.participated')}</span>
	{/if}
</div>
<p>{$t('research.info_url_introduction')} <a href="{data.research?.info_url}" target="_blank">{$t('research.here')}
	&nbsp;<span
			class="material-symbols-outlined">open_in_new</span></a></p>
{#each data.appointments as appointment, i}
	{@const when = new Date(appointment.when)
			.toLocaleString(undefined, {
				timeStyle: 'short',
				dateStyle: 'long'
			})}
	{@const is_signedup = $participations?.get(appointment.id) === false}
	<div class="{box}">
		<div class="{row} ver-center">
			<h2>{$t('research.appointment_number')} {i + 1}</h2>
			{#if appointment.location}
				<button>{$t('research.in_person')}</button>
			{:else}
				<button>{$t('research.online')}</button>
			{/if}
			{#if is_signedup}
				<button style="background: {vars.success}">{$t('research.appointment_signedup')}</button>
			{/if}
		</div>
		<p>{appointment.comment}</p>
		<table style="margin-bottom: {vars.sm}">
			<tr>
				<th>{$t('research.when')}</th>
				<th>{$t('research.capacity')}</th>
				{#if appointment.location}
					<th>{$t('research.location')}</th>
				{:else if is_signedup}
					<th>{$t('research.info_url')}</th>
				{/if}
			</tr>
			<tr>
				<td>{when}</td>
				<td><span style="color: {appointment.free_capacity ? 'initial' : 'red'}">{appointment.free_capacity}</span></td>
				{#if appointment.location}
					<td>{appointment.location}</td>
				{:else if is_signedup}
					<td>{appointment.info_url}</td>
				{/if}
			</tr>
		</table>
		{#if can_signup && appointment.free_capacity}
			<form method="POST" action="?/signup">
				<input type="hidden" name="appointment" value="{appointment.id}">
				<button type="submit">{$t('research.signup')}</button>
			</form>
		{/if}
		{#if is_signedup}
			<form method="POST" action="?/cancel">
				<button style="background: {vars.danger};">{$t('research.cancel')}</button>
			</form>
		{/if}
	</div>
{/each}