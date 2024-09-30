<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import Pagination from '$lib/components/Pagination.svelte';

	export let data: PageData;
</script>

<h1>EMPI</h1>
<div style="overflow-x: auto">
	<table style="width: 100%; max-width: 100vw">
		<tr>
			<th>{$t('research.name')}</th>
			<th>{$t('common.more_info')}</th>
			<th>{$t('common.details')}</th>
		</tr>
		{#each data.researches as research}
			{#if research.has_open_appointments}
				<tr>
					<td>{research.name}</td>
					<td style="text-align: center"><a href="{research.info_url}" target="_blank">{$t('common.learn_more')}</a>
					</td>
					<td style="text-align: center">
						<button>
							<a href="research/{research.id}/">{$t('common.details')}</a>
						</button>
					</td>
				</tr>
			{/if}
		{/each}
	</table>
</div>
<div class="row" style="margin-top: var(--sm)">
	<Pagination count={data.count}></Pagination>
</div>
