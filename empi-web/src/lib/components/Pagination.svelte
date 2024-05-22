<script lang="ts">
	import { page } from '$app/stores';
	import { PAGE_SIZE } from '$lib/constants';
	import MaterialSymbolsArrowBack from 'virtual:icons/material-symbols/arrow-back';
	import MaterialSymbolsArrowForward from 'virtual:icons/material-symbols/arrow-forward';

	export let count: number;
	$: limit = Number.parseInt($page.url.searchParams.get('limit')!) || PAGE_SIZE;
	$: offset = Number.parseInt($page.url.searchParams.get('offset')!) || 0;
</script>

{#if count > PAGE_SIZE}
	<div class="content row ver-center hor-center">
		<a href="?limit={limit}&offset={offset - limit}">
			<button disabled={offset - limit < 0}
			        aria-label="right arrow icon"
			        aria-describedby="previous">
				<MaterialSymbolsArrowBack width="24" height="24"></MaterialSymbolsArrowBack>
			</button>
		</a>
		<span>{offset + 1} - {Math.min(offset + limit, count)} of {count}</span>
		<a href="?limit={limit}&offset={offset + limit}">
			<button disabled={offset + limit > count}
			        aria-label="right arrow icon"
			        aria-describedby="next">
				<MaterialSymbolsArrowForward width="24" height="24"></MaterialSymbolsArrowForward>
			</button>
		</a>
	</div>
{/if}
