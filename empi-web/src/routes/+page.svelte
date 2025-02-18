<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import Pagination from '$lib/components/Pagination.svelte';
	import { onMount } from "svelte";

	let { data }: { data: PageData } = $props();
	let showInfoUrlColumn = $state(false);

	onMount(() => {
		for (const research of data.researches) {
			showInfoUrlColumn ||= research.info_url != null;
		}
	});
</script>

<h1>EMPI</h1>
<div style="overflow-x: auto">
	<table style="width: 100%; max-width: 100vw">
		<thead>
		<tr>
			<th>{$t('research.name')}</th>
			{#if showInfoUrlColumn}
				<th>{$t('common.more_info')}</th>
			{/if}
			<th>{$t('common.details')}</th>
		</tr>
		</thead>
		<tbody>
		{#each data.researches as research}
			{#if !research.all_appointments_closed}
				<tr>
					<td>{research.name}</td>
					{#if showInfoUrlColumn}
						<td style="text-align: center"><a href="{research.info_url}" target="_blank">{$t('common.learn_more')}</a>
						</td>
					{/if}
					<td style="text-align: center">
						<button>
							<a href="research/{research.id}/">{$t('common.details')}</a>
						</button>
					</td>
				</tr>
			{/if}
		{/each}
		</tbody>
	</table>
</div>
<div class="row" style="margin-top: var(--sm)">
	<Pagination count={data.count}></Pagination>
</div>
