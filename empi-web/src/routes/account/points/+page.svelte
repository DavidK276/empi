<script lang="ts">

	import { t } from '$lib/translations';
	import { page } from '$app/stores';

	const participations = $page.data.participations;
</script>

<h1>{$t('common.points')}</h1>
{#if participations != null && participations.length > 0}
	<div style="overflow-x: auto">
		<table style="width: 100%; max-width: 100vw">
			<thead>
			<tr>
				<th>{$t('common.research')}</th>
				<th>{$t('common.points')}</th>
				<th>{$t('research.participation')}</th>
			</tr>
			</thead>
			<tbody>
			{#each participations as participation}
				{@const research = participation.research}
				<tr>
					<td><a href="/research/{research?.id}">{research?.name}</a></td>
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
			</tbody>
		</table>
	</div>
{:else if participations != null && participations.length === 0}
	<p>{$t('research.no_points')}</p>
{/if}