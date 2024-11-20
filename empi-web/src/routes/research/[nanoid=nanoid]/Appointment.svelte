<script lang="ts">
	import type { Appointment } from '$lib/objects/appointment';
	import { t } from '$lib/translations';
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";

	let { appointment = null, nanoid }: { appointment: Appointment | null, nanoid: string } = $props();
	let thisComponent: HTMLFormElement | undefined = $state();
	let type: string = $state(appointment == null || appointment.info_url != null ? "online" : "in_person");
	let shown = $state(false);

	function formData(event: FormDataEvent) {
		const when = event.formData.get('when') as string;
		if (when) {
			event.formData.set('when', new Date(when).toISOString());
		}
		else {
			// we neet to set actual null here, but that is not allowed, so we set it to a special string and set actual null later
			event.formData.set('when', '__NULL__');
		}
	}

	onMount(() => shown = true);
</script>
{#if shown}
	<form bind:this={thisComponent} class="appointment-form" onformdata={formData} onsubmit={(e) => e.preventDefault()}
	      transition:slide={{duration: 200}} onoutroend={() => thisComponent?.parentNode?.removeChild(thisComponent)}>
		<div class="box">
			{#if appointment != null}
				<label for="type">{$t('research.appointment_type')}</label>
				<select id="type" bind:value={type}>
					<option value="online">{$t('research.online')}</option>
					<option value="in_person">{$t('research.in_person')}</option>
				</select>
				<label for="when">{$t('research.when')} ({$t('common.optional')})</label>
				<input type="datetime-local" name="when" id="when" value={appointment.getWhenLocal()}>
				<div style="display: flex; width: 100%; gap: var(--sm)">
					<div style="display: inline-flex; flex-direction: column; width: 50%">
						<label for="capacity">{$t('research.capacity')}</label>
						<input type="number" step="1" min="1" name="capacity" id="capacity" value={appointment.capacity}>
					</div>
					<div style="display: inline-flex; flex-direction: column; width: 50%">
						<label for="capacity">{$t('research.occupancy')}</label>
						<input type="text" readonly id="remaining" value="{appointment.capacity - appointment.free_capacity}">
					</div>
				</div>
				<label for="comment">{$t('research.comment')}</label>
				<textarea name="comment" id="comment">{appointment.comment}</textarea>
				{#if type === 'online'}
					<label for="info_url">{$t('research.appointment_url')}</label>
					<input type="url" name="info_url" id="info_url" maxlength="500" value={appointment.info_url}>
				{:else if type === 'in_person'}
					<label for="location">{$t('research.location')}</label>
					<input type="text" name="location" id="location" value={appointment.location}>
				{/if}
				<input type="hidden" name="id" value={appointment.id}>
			{:else}
				<label for="type">{$t('research.appointment_type')}</label>
				<select id="type" bind:value={type}>
					<option selected value="online">{$t('research.online')}</option>
					<option value="in_person">{$t('research.in_person')}</option>
				</select>
				<label for="when">{$t('research.when')}</label>
				<input type="datetime-local" name="when" id="when" required>
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
			<input name="research" type="hidden" value={nanoid}>
			<button onclick={() => shown = false}
			        style="background-color: var(--danger)">-
			</button>
		</div>
	</form>
{/if}