<script lang="ts">
	import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
	import { t } from '$lib/translations';
	import type { PageServerData } from './$types';

	export let data: PageServerData;

</script>
<UserPasswordRequiredModal></UserPasswordRequiredModal>
<h1>{$t('common.points')}</h1>
<div style="overflow-x: auto">
	<table style="width: 100%; max-width: 100vw">
		<tr>
			<th>{$t('common.name')}</th>
			<th>{$t('common.points')}</th>
		</tr>
		{#if data.participations}
			{#each data.participations.values() as participation}
				<tr>
					<td>{participation.name}</td>
					<td style="text-align: center">{participation.points}</td>
				</tr>
			{/each}
		{/if}
	</table>
</div>