<script lang="ts">
    import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
    import { t } from '$lib/translations';
    import type { PageServerData } from './$types';
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import { getCurrentAcademicYear, getCurrentSemester } from "$lib/settings";

    import { Datatable, TableHandler, ThFilter, ThSort } from '@vincjo/datatables'
		import { SvelteURLSearchParams } from 'svelte/reactivity';

    let { data }: { data: PageServerData } = $props();

    let selectedSemester = $state(page.url.searchParams.get('semester') || getCurrentSemester(page.data.settings));
    let selectedYear = $state(page.url.searchParams.get('year') || getCurrentAcademicYear(page.data.settings));

    function setSearchParams() {
        let query = new SvelteURLSearchParams(page.url.searchParams.toString());
        query.set('year', selectedYear);
        query.set('semester', selectedSemester);

        goto(`?${query.toString()}`, { invalidateAll: true });
    }
</script>
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div class="col" style="overflow-x: auto">
    <div class="row m-col" style="padding: var(--xs); white-space: nowrap">
        <div class="row" style="justify-content: space-between">
            <label for="year">Akad. rok</label>
            <select bind:value={selectedYear} id="year" onchange={setSearchParams} style="margin: 0; width: 16ch">
                {#each data.academic_year_choices as year (year)}
                    <option value="{year}">{year}</option>
                {/each}
            </select>
        </div>
        <div class="row" style="justify-content: space-between">
            <label for="semester">Semester</label>
            <select bind:value={selectedSemester} id="semester" onchange={setSearchParams}
                    style="margin: 0; width: 16ch">
                <option value="Z">zimný</option>
                <option value="L">letný</option>
                <option value="ANY">celý akad. rok</option>
            </select>
        </div>
    </div>
    {#await data.participations}
        <p>{$t('common.loading')}</p>
    {:then participations}
        <!-- the || undefined part is there to silence a warning -->
        {@const table = new TableHandler(participations || undefined, {rowsPerPage: 999, highlight: false})}
        {#if participations?.length || 0 > 0}
            <Datatable headless {table}>
                <table style="width: 100%; max-width: 100vw; border: none">
                    <thead>
                    <tr>
                        <ThSort {table} field="name">{$t('common.name')}</ThSort>
                        <ThSort {table} field="email">Email</ThSort>
                        <ThSort {table} field="unconfirmedPoints">{$t('common.unconfirmed_points')}</ThSort>
                        <ThSort {table} field="confirmedPoints">{$t('common.confirmed_points')}</ThSort>
                        <ThSort {table} field="totalPoints">{$t('common.sum')}</ThSort>
                    </tr>
                    <tr>
                        <ThFilter {table} field="name"></ThFilter>
                        <ThFilter {table} field="email"></ThFilter>
                        <ThFilter {table} field="unconfirmedPoints"></ThFilter>
                        <ThFilter {table} field="confirmedPoints"></ThFilter>
                        <ThFilter {table} field="totalPoints"></ThFilter>
                    </tr>
                    </thead>
                    <tbody>
										<!-- eslint-disable-next-line svelte/require-each-key -->
										{#each table.rows as row}
                        <tr>
                            <td>{row.name}</td>
                            <td>{row.email}</td>
                            <td style="text-align: center">{row.unconfirmedPoints}</td>
                            <td style="text-align: center">{row.confirmedPoints}</td>
                            <td style="text-align: center">{row.totalPoints}</td>
                        </tr>
                    {/each}
                    </tbody>
                </table>
            </Datatable>

        {:else}
            <p>{$t('common.no_students')}</p>
        {/if}
    {/await}
</div>

<style>
    select {
        margin: var(--sm) 0;
        width: fit-content;
    }
</style>
