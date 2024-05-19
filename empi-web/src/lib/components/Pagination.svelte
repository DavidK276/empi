<script lang="ts">
	import { page } from '$app/stores';
	import { PAGE_SIZE } from '$lib/constants';
	import Icon from "@iconify/svelte";

	export let count: number;
	$: limit = Number.parseInt($page.url.searchParams.get('limit')!) || PAGE_SIZE;
	$: offset = Number.parseInt($page.url.searchParams.get('offset')!) || 0;
</script>

{#if count <= PAGE_SIZE}
	<div class="content container row ver-center hor-center">
		<a href="?limit={limit}&offset={offset - limit}">
			<button disabled={offset - limit < 0}
			        aria-label="right arrow icon"
			        aria-describedby="previous">
				<Icon icon="material-symbols:arrow-back" width="24" height="24"></Icon>
			</button>
		</a>
		<span>{offset + 1} - {Math.min(offset + limit, count)} of {count}</span>
		<a href="?limit={limit}&offset={offset + limit}">
			<button disabled={offset + limit > count}
			        aria-label="right arrow icon"
			        aria-describedby="next">
				<Icon icon="material-symbols:arrow-forward" width="24" height="24"></Icon>
			</button>
		</a>
	</div>
{/if}
