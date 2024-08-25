<script lang="ts">

	import { t } from '$lib/translations';
	import { page } from '$app/stores';
	import type { PageData } from './$types';

	export let data: PageData;

	const participations = $page.data.participations;
</script>

<h1>{$t('common.points')}</h1>
{#if participations != null && participations.length > 0}
	<div style="overflow-x: auto">
		<table style="width: 100%; max-width: 100vw">
			<tr>
				<th>{$t('research.name')}</th>
				<th>{$t('common.more_info')}</th>
				<th>{$t('common.points')}</th>
				<th>{$t('research.participation')}</th>
			</tr>
			{#each participations as participation}
				{@const research = data.researches.get(participation.research)}
				<tr>
					<td>{research?.name}</td>
					<td style="text-align: center"><a href="{research?.info_url}" target="_blank">{$t('common.learn_more')}</a></td>
					{#if research?.points != null}
						<td style="text-align: center">{research.points}</td>
					{:else}
						<td style="text-align: center">?</td>
					{/if}
					{#if participation.is_confirmed}
						<td style="text-align: center">{$t('research.yes')} ✅</td>
					{:else}
						<td style="text-align: center">{$t('research.notyet')}</td>
					{/if}
				</tr>
			{/each}
		</table>
	</div>
{:else if participations != null && participations.length === 0}
	<p>{$t('research.no_points')}</p>
{/if}