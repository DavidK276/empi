<script lang="ts">
	import type { IParticipation } from "$lib/objects/participation";
	import Participation from "$lib/components/Participation.svelte";
	import { t } from '$lib/translations';


	let { participations }: {
		participations: { confirmed: IParticipation[], unconfirmed: IParticipation[] }
	} = $props();
</script>
{#if participations.confirmed.length > 0 || participations.unconfirmed.length > 0}
	{#if participations.unconfirmed.length > 0}
		<div class="col" style="margin-bottom: var(--sm)">
			<h2 style="width: 100%; margin: 0">Nepotvrdené účasti</h2>
			<div style="display: flex; gap: var(--md); flex-wrap: wrap">
				{#each participations.unconfirmed as participation (participation.id)}
					<Participation {participation}></Participation>
				{:else}
					<p>{$t('research.no_participations')}</p>
				{/each}
			</div>
		</div>
	{/if}
	{#if participations.confirmed.length > 0}
		<div class="col" style="margin-bottom: var(--sm)">
			<h2 style="width: 100%; margin: 0">Potvrdené účasti</h2>
			<div style="display: flex; gap: var(--md); flex-wrap: wrap">
				{#each participations.confirmed as participation (participation.id)}
					<Participation {participation}></Participation>
				{:else}
					<p>{$t('research.no_participations')}</p>
				{/each}
			</div>
		</div>
	{/if}
{:else}
	<p>{$t('research.no_participations')}</p>
{/if}