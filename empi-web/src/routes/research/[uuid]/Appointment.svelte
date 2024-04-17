<script lang="ts">
	import type { Appointment } from '$lib/objects/appointment';
	import { t } from '$lib/translations';
	import { vars } from '$lib/theme.css';
	import { box } from '$lib/style.css';

	export let appointment: Appointment | null = null;
	export let uuid: string;
	let nodeRef: HTMLElement;
	let type: string;
</script>
<form bind:this={nodeRef} on:submit|preventDefault class="appointment-form">
	<div class="{box}">
		{#if appointment != null}
			<label for="type">{$t('research.appointment_type')}</label>
			<select id="type" bind:value={type}>
				<option selected="{appointment.info_url != null}" value="online">{$t('research.online')}</option>
				<option selected="{appointment.location != null}" value="in_person">{$t('research.in_person')}</option>
			</select>
			<label for="when">{$t('research.when')}</label>
			<input type="datetime-local" name="when" id="when"
						 value="{new Date(appointment.when).toISOString().slice(0, -1)}">
			<label for="capacity">{$t('research.capacity')}</label>
			<input type="number" step="1" name="capacity" id="capacity" value="{appointment.capacity}">
			<label for="comment">{$t('research.comment')}</label>
			<textarea name="comment" id="comment">{appointment.comment}</textarea>
			{#if type === 'online'}
				<label for="info_url">{$t('research.appointment_url')}</label>
				<input type="url" name="info_url" id="info_url" value="{appointment.info_url}">
			{:else if type === 'in_person'}
				<label for="location">{$t('research.location')}</label>
				<input type="text" name="location" id="location" value="{appointment.location}">
			{/if}
			<input type="hidden" name="id" value="{appointment.id}">
		{:else}
			<label for="type">{$t('research.appointment_type')}</label>
			<select id="type" bind:value={type}>
				<option selected value="online">{$t('research.online')}</option>
				<option value="in_person">{$t('research.in_person')}</option>
			</select>
			<label for="when">{$t('research.when')}</label>
			<input type="datetime-local" name="when" id="when">
			<label for="capacity">{$t('research.capacity')}</label>
			<input type="number" step="1" name="capacity" id="capacity">
			<label for="comment">{$t('research.comment')}</label>
			<textarea name="comment" id="comment"></textarea>
			{#if type === 'online'}
				<label for="info_url">{$t('research.appointment_url')}</label>
				<input type="url" name="info_url" id="info_url">
			{:else if type === 'in_person'}
				<label for="location">{$t('research.location')}</label>
				<input type="text" name="location" id="location">
			{/if}
		{/if}
		<input type="hidden" name="research" value="{uuid}">
		<button style="background-color: {vars.danger}" on:click={() => nodeRef.parentNode?.removeChild(nodeRef)}>-</button>
	</div>
</form>