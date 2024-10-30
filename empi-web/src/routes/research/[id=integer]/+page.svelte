<script lang="ts">
	import showdown from 'showdown';
	import DOMPurify from 'dompurify';
	import type { PageData } from './$types';
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import { page } from '$app/stores';
	import { browser } from "$app/environment";
	import { enhance } from '$app/forms';
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import { localeDateStringFromUTCString } from '$lib/functions';
	import { universalEnhance } from "$lib/enhanceFunctions";

	let { data }: { data: PageData } = $props();

	const converter = new showdown.Converter();
	let sanitizedComment = $state("");
	if (browser && data.research?.comment) {
		sanitizedComment = DOMPurify.sanitize(converter.makeHtml(data.research?.comment), { USE_PROFILES: { html: true } });
	}
</script>
{#if $page.data.user != null}
	<UserPasswordRequiredModal></UserPasswordRequiredModal>
{/if}
<div class="row m-col">
	<h1 style="display: inline; margin: 0">{data.research?.name}</h1>
	{#if data.isConfirmed}
		<p class="message">
			<MaterialSymbolsInfoOutline width="24"
			                            height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.participated')}</p>
	{/if}
</div>

<!-- eslint-disable-next-line svelte/no-at-html-tags The html in this variable IS sanitized. -->
{@html sanitizedComment}
{#if data.research?.info_url}
	<p>{$t('research.info_url_introduction')} <a href={data.research?.info_url} target="_blank">{$t('research.here')}</a>
	</p>
{/if}
{#each data.appointments as appointment, i}
	{@const participation = $page.data.participations?.get(appointment.id)}
	{@const is_confirmed = participation?.is_confirmed === true}
	{@const signups_lapsed = new Date(appointment.when) < new Date()}
	<div class="box">
		<div class="row ver-center">
			<h2>{$t('research.appointment_number')} {i + 1}</h2>
			{#if appointment.location}
				<button>{$t('research.in_person')}</button>
			{:else}
				<button>{$t('research.online')}</button>
			{/if}
			{#if participation != null}
				<button style="background: var(--success)">{$t('research.appointment_signedup')}</button>
			{/if}
			{#if signups_lapsed}
				<p class="message">
					<MaterialSymbolsInfoOutline width="24"
					                            height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.signups_lapsed')}</p>
			{/if}
		</div>
		<p>{appointment.comment}</p>
		<div style="width: 50%" class="m-w-full">
			<table style="width: 100%; margin-bottom: var(--sm)">
				<thead>
				<tr>
					<th>{$t('research.when')}</th>
					{#if appointment.location}
						<th>{$t('research.location')}</th>
					{:else if participation != null && !is_confirmed}
						<th>{$t('research.join_appointment_url')}</th>
					{/if}
					<th>{$t('research.free_capacity')}</th>
				</tr>
				</thead>
				<tbody>
				<tr>
					<td>
						<time datetime="{appointment.when}">{localeDateStringFromUTCString(appointment.when)}</time>
					</td>
					{#if appointment.location}
						<td>{appointment.location}</td>
					{:else if participation != null && !is_confirmed}
						<td><a href={appointment.info_url} target="_blank">{$t('research.join_appointment')}</a></td>
					{/if}
					<td style="text-align: center">
						<span
								style="color: {appointment.free_capacity ? 'var(--text-primary)' : 'red'}">{appointment.free_capacity}</span>
					</td>
				</tr>
				</tbody>
			</table>
			{#if data.canSignup && appointment.free_capacity > 0 && !signups_lapsed}
				<form method="POST" action="?/signup" use:enhance={({formElement, submitter}) => {
					return universalEnhance({formElement, submitter}, {
						idleMessage: $t('common.login'),
						runningMessage: $t('common.logging_in'),
						reset: false,
						invalidateAll: true
					});
				}}>
					<input type="hidden" name="appointment" value={appointment.id}>
					{#if $page.data.user == null}
						<label for="recipient">Email</label>
						<input type="email" name="recipient" id="recipient" class="m-w-full">
					{/if}
					<div class="row ver-center" id="submit-div">
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
			{#if participation != null && !is_confirmed}
				<form method="POST" action="?/cancel" use:enhance={({formElement, submitter}) => {
					return universalEnhance({formElement, submitter}, {
						idleMessage: $t('common.logout'),
						runningMessage: $t('common.logging_out'),
						reset: false,
						invalidateAll: true
					});
				}}>
					<input type="hidden" name="participation-id" value={participation?.id}>
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