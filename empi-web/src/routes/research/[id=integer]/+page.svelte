<script lang="ts">
	import type { ActionData, PageData } from './$types';
	import PasswordRequiredModal from '$lib/components/PasswordRequiredModal.svelte';
	import { box, row } from '$lib/style.css';
	import { t } from '$lib/translations';
	import { store } from '$lib/stores';
	import { page } from '$app/stores';
	import { type Writable, writable } from 'svelte/store';
	import { vars } from '$lib/theme.css';
	import type { Participation } from '$lib/objects/participation';
	import { onMount } from 'svelte';
	import { goto, invalidateAll } from '$app/navigation';

	export let data: PageData;
	export let form: ActionData;

	store.subscribe(() => getSignups());

	async function getSignups() {
		if (!$store.password) {
			return;
		}
		const formData = new FormData();
		formData.set('current_password', $store.password);
		const href = new URL(document.location.href);
		const response = await fetch(href.origin, { method: 'POST', body: formData });
		const responseJSON = await response.json() as Array<{
			appointment: number,
			has_participated: boolean,
			research: number
		}>;
		const participationMap = new Map();
		for (const participation of responseJSON) {
			if (participation.research === data.research?.id) {
				participationMap.set(participation.appointment, participation);
				can_signup = false;
				has_participated ||= participation.has_participated;
			}
		}
		participations.set(participationMap);
	}

	async function cancelSignup(event: Event) {
		const form = event.target as HTMLFormElement;
		const formData = new FormData(form);
		formData.set('current_password', $store.password);
		const participationId = formData.get('participation')!;
		formData.delete('participation');

		const href = new URL(document.location.href);
		const url = href.origin + `/participation/${participationId}/`;
		await fetch(url, { method: 'POST', body: formData });

		await invalidateAll();
		await getSignups();
		can_signup = true;
		has_participated = false;
	}

	onMount(() => {
		if (form?.success && form.participation != null) {
			goto(`/participation/${form.participation.uuid}/`);
		}
	});

	let participations: Writable<Map<number, Participation>> = writable();
	let can_signup = true;
	let has_participated = false;
</script>
{#if $page.data.user != null}
	<PasswordRequiredModal></PasswordRequiredModal>
{/if}
<div class="{row} m-col">
	<h1 style="display: inline; margin: 0">{data.research?.name}</h1>
	{#if has_participated}
		<span style="display: inline-flex; align-items: center"><span
			class="material-symbols-outlined">info</span>&nbsp{$t('research.participated')}</span>
	{/if}
</div>
<p>{$t('research.info_url_introduction')} <a href={data.research?.info_url} target="_blank">{$t('research.here')}
	&nbsp;<span
		class="material-symbols-outlined">open_in_new</span></a></p>
{#each data.appointments as appointment, i}
	{@const when = new Date(appointment.when)
		.toLocaleString(undefined, {
			timeStyle: 'short',
			dateStyle: 'long'
		})}
	{@const participation = $participations?.get(appointment.id)}
	{@const is_signedup = participation?.has_participated === false}
	<div class={box}>
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
				<input type="hidden" name="appointment" value={appointment.id}>
				<div class={row}>
					<button type="submit">{$t('research.signup')}</button>
					{#if $page.data.user == null}
						<p style="display: inline-flex; margin: 0; align-items: center"><span
							class="material-symbols-outlined">info</span>&nbsp;{$t('research.anonymous_signup')}</p>
					{/if}
				</div>
			</form>
		{/if}
		{#if is_signedup}
			<form method="POST" on:submit|preventDefault={cancelSignup}>
				<input type="hidden" name="participation" value={participation?.id}>
				<button type="submit" style="background: {vars.danger};">{$t('research.cancel')}</button>
			</form>
		{/if}
	</div>
{/each}