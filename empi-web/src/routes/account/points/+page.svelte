<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import { store } from '$lib/stores';
	import { type Writable, writable } from 'svelte/store';
	import { Participation } from '$lib/objects/participation';
	import type { PageData } from './$types';

	export let data: PageData;

	store.subscribe(async ({ user_password }) => {
		if (!user_password) {
			return;
		}

		const formData = new FormData();
		formData.set('current_password', user_password);
		const response = await fetch('/server/participations/user', { method: 'POST', body: formData });
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
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
{#if $participations != null && $participations.length > 0}
	<div style="overflow-x: auto">
		<table style="width: 100%; max-width: 100vw">
			<tr>
				<th>{$t('research.name')}</th>
				<th>{$t('common.more_info')}</th>
				<th>{$t('common.points')}</th>
				<th>{$t('research.participation')}</th>
			</tr>
			{#each $participations as participation}
				{@const research = data.researches.get(participation.research)}
				<tr>
					<td>{research?.name}</td>
					<td><a href="{research?.info_url}">{$t('common.learn_more')}</a></td>
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
		</table>
	</div>
{:else if $participations != null && $participations.length === 0}
	<p>{$t('research.no_points')}</p>
{/if}