<script lang="ts">
	import showdown from 'showdown';
	import DOMPurify from 'dompurify';
	import Pagination from '$lib/components/Pagination.svelte';
	import { t } from '$lib/translations';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import type { PageServerData } from './$types';
	import { base } from "$app/paths";
	import { browser } from "$app/environment";

	onMount(() => {
		if (!$page.data.user?.is_staff) {
			goto(`${base}/`, { replaceState: true });
		}
	});

	let { data }: { data: PageServerData } = $props();
	const converter = new showdown.Converter();
</script>
<h1>{$t('common.research_list')}</h1>
{#if data.researches != null}
	{#each data.researches as research}
		<div class="box">
			<h1>{research.name}</h1>
			{#if browser && research.comment}
				<div class="box">
					{@html DOMPurify.sanitize(converter.makeHtml(research.comment), {USE_PROFILES: {html: true}})}
				</div>
			{/if}
			<a href="{base}/research/{research.nanoid}">
				<button type="button">Spravovať</button>
			</a>
		</div>
	{/each}
{/if}
<Pagination count={data.count}></Pagination>

<a href="{base}/research">
	<button>{$t('common.add_research')}</button>
</a>