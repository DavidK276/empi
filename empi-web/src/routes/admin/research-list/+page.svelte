<script lang="ts">
	import Markdown from 'svelte-exmarkdown';
	import Pagination from '$lib/components/Pagination.svelte';
	import { t } from '$lib/translations';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import type { PageProps } from './$types';
	import { resolve } from "$app/paths";
	import { browser } from "$app/environment";

	onMount(() => {
		if (!page.data.user?.is_staff) {
			goto(resolve('/'), { replaceState: true });
		}
	});

	let { data }: PageProps = $props();
</script>
<h1>{$t('common.research_list')}</h1>
{#if data.researches != null}
	{#each data.researches as research (research.nanoid)}
		<div class="box">
			<h1>{research.name}</h1>
			{#if browser && research.comment}
				<div class="box">
					<Markdown md={research.comment}></Markdown>
				</div>
			{/if}
			<a href="{resolve('/research/[nanoid=nanoid]', {nanoid: research.nanoid})}">
				<button type="button">{$t('common.manage')}</button>
			</a>
		</div>
	{/each}
{/if}
<Pagination count={data.count}></Pagination>

<a href="{resolve('/research')}">
	<button>{$t('common.add_research')}</button>
</a>
