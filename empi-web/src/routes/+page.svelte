<script lang="ts">
	import type { PageData } from './$types';
	import { t } from '$lib/translations';
	import { page } from '$app/stores';
	import { vars } from '$lib/theme.css';

	export let data: PageData;
</script>

<h1>EMPI</h1>
<table style="width: 100%">
	<tr>
		<th>{$t('research.name')}</th>
		<th>{$t('research.info_url')}</th>
		{#if $page.data.user != null}
			<th>{$t('common.details')}</th>
		{/if}
	</tr>
	{#each data.researches as research}
		<tr>
			<td>{research.name}</td>
			<td>{research.info_url}</td>
			{#if $page.data.user != null}
				<th>
					<button>
						<a href="research/{research.id}/" style="color: {vars.textSecondary}">{$t('common.details')}</a>
					</button>
				</th>
			{/if}
		</tr>
	{/each}
</table>
