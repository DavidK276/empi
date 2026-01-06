<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import Pagination from '$lib/components/Pagination.svelte';

	let { data }: { data: PageData } = $props();
	let showInfoUrlColumn = $derived(data.researches.some(r => r.has_open_appointments && r.info_url));
</script>

<h1>EMPI <span style="font-weight: normal">- Účasť na Empirickom Výskume (2-MXX-132)</span></h1>
<div style="overflow-x: auto">
	<h2>{$t('common.current_published_research')}</h2>
	<table style="width: 100%; max-width: 100vw">
		<thead>
		<tr>
			<th>{$t('research.name')}</th>
			{#if showInfoUrlColumn}
				<th>{$t('common.info_url')}</th>
			{/if}
			<th>{$t('common.details')}</th>
		</tr>
		</thead>
		<tbody>
		{#each data.researches as research (research.id)}
			{#if research.has_open_appointments}
				<tr>
					<td>{research.name}</td>
					{#if showInfoUrlColumn}
						<td style="text-align: center">
							{#if research.info_url}<a href="{research.info_url}" target="_blank">{$t('common.learn_more')}</a>{:else}
								N/A
							{/if}
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
