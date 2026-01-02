<script lang="ts">
	import type { PageProps } from './$types';

	import { t } from '$lib/translations';
	import { page } from '$app/state';
	import { getCurrentAcademicYear, getCurrentSemester } from "$lib/settings";
	import { goto } from "$app/navigation"
	import { SvelteURLSearchParams } from 'svelte/reactivity';
	import { resolve } from "$app/paths";

	let { data }: PageProps = $props();
	let query = new SvelteURLSearchParams(page.url.searchParams.toString());


	let selectedSemester = $state(query.get('semester') || getCurrentSemester(page.data.settings));
	let selectedYear = $state(query.get('year') || getCurrentAcademicYear(page.data.settings));

	$effect(() => {
		query.set('year', selectedYear);
		query.set('semester', selectedSemester);

		goto(`?${query.toString()}`, { invalidateAll: true });
	});
</script>

<h1>{$t('common.points')}</h1>
<div class="col" style="overflow-x: auto">
	<div class="row m-col" style="padding: var(--xs); white-space: nowrap">
		<div class="row" style="justify-content: space-between">
			<label for="year">Akad. rok</label>
			<select bind:value={selectedYear} id="year" style="margin: 0; width: 16ch">
				{#each data.academic_year_choices as year (year)}
					<option value="{year}">{year}</option>
				{/each}
			</select>
		</div>
		<div class="row" style="justify-content: space-between">
			<label for="semester">Semester</label>
			<select bind:value={selectedSemester} id="semester" style="margin: 0; width: 16ch">
				<option value="Z">zimný</option>
				<option value="L">letný</option>
				<option value="ANY">celý akad. rok</option>
			</select>
		</div>
	</div>
	{#await data.participations}
		<p>{$t('common.loading')}</p>
	{:then participations}
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
					{#each participations as participation (participation.id)}
						{@const research = participation.research}
						<tr>
							<td><a
								href="{resolve('/research/[id=integer]', {id: research.id + ''})}">{research.name}</a>
							</td>
							{#if research.points != null}
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
	{/await}
</div>
