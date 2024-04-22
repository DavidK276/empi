<script lang="ts">
	import PasswordRequiredModal from '$lib/components/PasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import { store } from '$lib/stores';
	import { type Writable, writable } from 'svelte/store';
	import { Participation } from '$lib/objects/participation';
	import type { PageData } from './$types';

	export let data: PageData;

	store.subscribe(async ({ password }) => {
		if (!password) {
			return;
		}

		const formData = new FormData();
		formData.set('current_password', password);
		const href = new URL(document.location.href);
		const response = await fetch(href.origin, { method: 'POST', body: formData });
		const responseJSON = await response.json() as Array<{
			appointment: number,
			has_participated: boolean,
			research: number
		}>;
		const participationMap: Participation[] = [];
		for (const participationData of responseJSON) {
			const participation = new Participation();
			Object.assign(participation, participationData);
			participationMap.push(participation);
		}
		participations.set(participationMap);
	});

	let participations: Writable<Participation[]> = writable();
</script>
<PasswordRequiredModal></PasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div style="overflow-x: auto">
	<table style="width: 100%">
	<tr>
		<th>{$t('research.name')}</th>
		<th>{$t('research.info_url')}</th>
		<th>{$t('common.points')}</th>
		<th>{$t('research.participation')}</th>
	</tr>
	{#if $participations != null}
		{#each $participations as participation}
			{@const research = data.researches.get(participation.research)}
			<tr>
				<td>{research?.name}</td>
				<td>{research?.info_url}</td>
				{#if research?.points != null}
					<td style="text-align: center">{research.points}</td>
				{:else}
					<td style="text-align: center">?</td>
				{/if}
				{#if participation.has_participated}
					<td style="text-align: center">{$t('research.yes')} ✅</td>
				{:else}
					<td style="text-align: center">{$t('research.notyet')}</td>
				{/if}
			</tr>
		{/each}
	{/if}
</table>
</div>