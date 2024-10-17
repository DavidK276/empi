<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import { localeDateStringFromUTCString } from "$lib/functions";

	export let data: PageData;

	const appointment = data.appointment;
</script>

<div class="box">
	<div class="row ver-center">
		<h2>{$t('research.appointment')}</h2>
		{#if appointment.location}
			<button>{$t('research.in_person')}</button>
		{:else}
			<button>{$t('research.online')}</button>
		{/if}
		<button style="background: var(--success)">{$t('research.appointment_signedup')}</button>
	</div>
	<p>{appointment.comment}</p>
	<table style="margin-bottom: var(--sm)">
		<tr>
			<th>{$t('research.when')}</th>
			<th>{$t('research.capacity')}</th>
			{#if appointment.location}
				<th>{$t('research.location')}</th>
			{:else}
				<th>{$t('research.join_appointment_url')}</th>
			{/if}
		</tr>
		<tr>
			<td><time datetime="{appointment.when}">{localeDateStringFromUTCString(appointment.when)}</time></td>
			<td><span class:danger={appointment.free_capacity === 0}>{appointment.free_capacity}</span></td>
			{#if appointment.location}
				<td>{appointment.location}</td>
			{:else}
				<td><a href={appointment.info_url} target="_blank">{$t('research.join_appointment')}</a></td>
			{/if}
		</tr>
	</table>
	<form method="POST" action="?/cancel">
		<button type="submit" style="background: var(--danger)">{$t('research.cancel')}</button>
	</form>
</div>