<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import type { PageServerData } from './$types';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { getCurrentAcademicYear, getCurrentSemester } from "$lib/settings";

	let { data }: { data: PageServerData } = $props();

	let selectedSemester = $state(page.url.searchParams.get('semester') || getCurrentSemester(page.data.settings));
	let selectedYear = $state(page.url.searchParams.get('year') || getCurrentAcademicYear(page.data.settings));

	function setSearchParams() {
		let query = new URLSearchParams(page.url.searchParams.toString());
		query.set('year', selectedYear);
		query.set('semester', selectedSemester);

		goto(`?${query.toString()}`, { invalidateAll: true });
	}

	data.participations?.sort((a, b) => {
		const textA = a.name.toUpperCase().split(' ', 2)[1];
		const textB = b.name.toUpperCase().split(' ', 2)[1];
		return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
	})
</script>
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div style="overflow-x: auto">
	<div class="row m-col" style="padding: var(--xs)">
		<div class="row" style="justify-content: space-between">
			<label for="year">Rok</label>
			<input bind:value={selectedYear} id="year" onchange={setSearchParams} type="text">
		</div>
		<div class="row" style="justify-content: space-between">
			<label for="semester">Semester</label>
			<select bind:value={selectedSemester} id="semester" onchange={setSearchParams}>
				<option value="Z">zimný</option>
				<option value="L">letný</option>
			</select>
		</div>
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