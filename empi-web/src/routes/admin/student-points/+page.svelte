<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import type { PageServerData } from './$types';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	export let data: PageServerData;

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

	let selectedSemester = $page.url.searchParams.get('semester') || getCurrentSemester();
	let selectedYear = $page.url.searchParams.get('year') || new Date().getFullYear();

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
		<input type="number" step="1" min="2024" id="year" bind:value={selectedYear} on:change={setSearchParams}>
		<label for="semester">Semester</label>
		<select id="semester" bind:value={selectedSemester} on:change={setSearchParams}>
			<option value="z">zimný</option>
			<option value="l">letný</option>
		</select>
	</div>
	{#if data.participations && data.participations.length > 0}
		<table style="width: 100%; max-width: 100vw">
			<tr>
				<th>{$t('common.name')}</th>
				<th>{$t('common.unconfirmed_points')}</th>
				<th>{$t('common.confirmed_points')}</th>
				<th>{$t('common.sum')}</th>
			</tr>
			{#each data.participations as participation}
				<tr>
					<td>{participation.name}</td>
					<td style="text-align: center">{participation.unconfirmedPoints}</td>
					<td style="text-align: center">{participation.confirmedPoints}</td>
					<td style="text-align: center">{participation.unconfirmedPoints + participation.confirmedPoints}</td>
				</tr>
			{/each}
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