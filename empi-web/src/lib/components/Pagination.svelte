<script lang="ts">
	import { content, row } from '$lib/style.css';
	import { PAGE_SIZE } from '$lib/constants';
	export let allRows;
	export let currentPageRows;

	$: totalRows = allRows.length;
	$: currentPage = 0;
	$: totalPages = Math.ceil(totalRows / PAGE_SIZE);
	$: start = currentPage * PAGE_SIZE;
	$: end = currentPage === totalPages - 1 ? totalRows - 1 : start + PAGE_SIZE - 1;

	$: currentPageRows = allRows.slice(start, end + 1);

	$: totalRows, currentPage = 0;
	$: currentPage, start, end;

</script>

{#if totalRows && totalRows > PAGE_SIZE}
	<div class="{content} {row} ver-center hor-center">
		<button on:click={() => currentPage -= 1}
						disabled={currentPage === 0}
						aria-label="left arrow icon"
						aria-describedby="prev">
			<span class="material-symbols-outlined">arrow_back</span>
		</button>
		<span>{start + 1} - {end + 1} of {totalRows}</span>
		<button on:click={() => currentPage += 1}
						disabled={currentPage === totalPages - 1}
						aria-label="right arrow icon"
						aria-describedby="next">
			<span class="material-symbols-outlined">arrow_forward</span>
		</button>
	</div>
{/if}
