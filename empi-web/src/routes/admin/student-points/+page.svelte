<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import { store } from '$lib/stores';
	import { type Writable, writable } from 'svelte/store';
	import { Participation } from '$lib/objects/participation';
	import type { PageData } from './$types';
	import { plainToInstance } from 'class-transformer';

	export let data: PageData;

	store.subscribe(async ({ user_password }) => {
		if (!user_password) {
			return;
		}

		const formData = new FormData();
		formData.set('current_password', user_password);
		const href = new URL(document.location.href);
		const response = await fetch(href.origin, { method: 'POST', body: formData });
		const responseJSON = await response.json() as Array<{
			appointment: number,
			has_participated: boolean,
			research: number
		}>;

		const pointMap: Map<string, number> = new Map();
		const participations = plainToInstance(Participation, responseJSON);
		for (const participation of participations) {
			const research = data.researches.get(participation.research);
			const participant = data.participants.get(participation.token!);
			if (research != null && participant != null) {
				const user = data.users.get(participant.user);
				if (user != null) {
					const name = user.first_name + ' ' + user.last_name;
					let currentPoints = pointMap.get(name);
					currentPoints = (currentPoints != null) ? currentPoints : 0;
					currentPoints += research.points;
					pointMap.set(name, currentPoints);
				}
			}
		}
		points.set(pointMap);
	});

	let points: Writable<Map<string, number>> = writable();
</script>
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div style="overflow-x: auto">
	<table style="width: 100%">
		<tr>
			<th>{$t('common.name')}</th>
			<th>{$t('common.points')}</th>
		</tr>
		{#if $points != null}
			{#each $points as point}
				<tr>
					<td>{point[0]}</td>
					<td style="text-align: center">{point[1]}</td>
				</tr>
			{/each}
		{/if}
	</table>
</div>