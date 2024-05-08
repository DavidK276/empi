<script lang="ts">
  import type { PageData } from './$types';
  import { box, row } from '$lib/style.css';
  import { t } from '$lib/translations';
  import { vars } from '$lib/theme.css';

  export let data: PageData;

  const appointment = data.appointment;
  const when = new Date(appointment.when)
    .toLocaleString(undefined, {
      timeStyle: 'short',
      dateStyle: 'long'
    });
</script>

<div class={box}>
	<div class="{row} ver-center">
		<h2>{$t('research.appointment')}</h2>
		{#if appointment.location}
			<button>{$t('research.in_person')}</button>
		{:else}
			<button>{$t('research.online')}</button>
		{/if}
		<button style="background: {vars.success}">{$t('research.appointment_signedup')}</button>
	</div>
	<p>{appointment.comment}</p>
	<table style="margin-bottom: {vars.sm}">
		<tr>
			<th>{$t('research.when')}</th>
			<th>{$t('research.capacity')}</th>
			{#if appointment.location}
				<th>{$t('research.location')}</th>
			{:else}
				<th>{$t('research.info_url')}</th>
			{/if}
		</tr>
		<tr>
			<td>{when}</td>
			<td><span style="color: {appointment.free_capacity ? 'initial' : 'red'}">{appointment.free_capacity}</span></td>
			{#if appointment.location}
				<td>{appointment.location}</td>
			{:else}
				<td>{appointment.info_url}</td>
			{/if}
		</tr>
	</table>
	<form method="POST" action="?/cancel">
		<button type="submit" style="background: {vars.danger};">{$t('research.cancel')}</button>
	</form>
</div>