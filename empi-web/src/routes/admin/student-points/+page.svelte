<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import type { PageServerData } from './$types';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	let { data }: { data: PageServerData } = $props();

	function getCurrentSemester() {
		const month = new Date().getMonth();
		return month >= 7 ? 'z' : 'l';
	}

	function setSearchParams() {
		let query = new URLSearchParams($page.url.searchParams.toString());
		query.set('year', selectedYear.toString());
		query.set('semester', selectedSemester);

		goto(`?${query.toString()}`, { invalidateAll: true });
	}

	let selectedSemester = $state($page.url.searchParams.get('semester') || getCurrentSemester());
	let selectedYear = $state($page.url.searchParams.get('year') || new Date().getFullYear());

	data.participations?.sort((a, b) => {
		const textA = a.name.toUpperCase().split(' ', 2)[1];
		const textB = b.name.toUpperCase().split(' ', 2)[1];
		return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
	})
</script>
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div style="overflow-x: auto">
	<div class="row" style="padding: var(--xs)">
		<label for="year">Rok</label>
		<input bind:value={selectedYear} id="year" min="2024" onchange={setSearchParams} step="1" type="number">
		<label for="semester">Semester</label>
		<select bind:value={selectedSemester} id="semester" onchange={setSearchParams}>
			<option value="z">zimný</option>
			<option value="l">letný</option>
		</select>
	</div>
	{#if data.participations && data.participations.length > 0}
		<table style="width: 100%; max-width: 100vw">
			<thead>
			<tr>
				<th>{$t('common.name')}</th>
				<th>{$t('common.unconfirmed_points')}</th>
				<th>{$t('common.confirmed_points')}</th>
				<th>{$t('common.sum')}</th>
			</tr>
			</thead>
			<tbody>
			{#each data.participations as participation}
				<tr>
					<td>{participation.name}</td>
					<td style="text-align: center">{participation.unconfirmedPoints}</td>
					<td style="text-align: center">{participation.confirmedPoints}</td>
					<td style="text-align: center">{participation.unconfirmedPoints + participation.confirmedPoints}</td>
				</tr>
			{/each}
			</tbody>
		</table>
	{:else}
		<p>{$t('common.no_students')}</p>
	{/if}
</div>

<style>
    input, select {
        margin: var(--sm) 0;
        width: fit-content;
    }
</style>