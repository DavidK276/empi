<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import Pagination from '$lib/components/Pagination.svelte';
	import Icon from "@iconify/svelte";

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
			<tr>
				<td>{research.name}</td>
				<td style="text-align: center"><a href="{research.info_url}" target="_blank">{$t('common.learn_more')}
					<Icon icon="material-symbols:open-in-new" width="24" height="24"></Icon>
				</a></td>
				<td style="text-align: center">
					<button>
						<a href="research/{research.id}/">{$t('common.details')}</a>
					</button>
				</td>
			</tr>
		{/each}
	</table>
</div>
<div class="row" style="margin-top: var(--sm)">
	<Pagination count={data.count}></Pagination>
</div>
