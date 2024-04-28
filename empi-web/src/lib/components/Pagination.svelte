<script lang="ts">
	import { content, row } from '$lib/style.css';
	import { page } from '$app/stores';
	import { PAGE_SIZE } from '$lib/constants';

	export let count;
	$: limit = Number.parseInt($page.url.searchParams.get('limit')!) || PAGE_SIZE;
	$: offset = Number.parseInt($page.url.searchParams.get('offset')!) || 0;
</script>

<div class="{content} {row} ver-center hor-center">
	<a href="?limit={limit}&offset={offset - limit}">
		<button disabled={offset - limit < 0}
						aria-label="right arrow icon"
						aria-describedby="next">
			<span class="material-symbols-outlined">arrow_back</span>
		</button>
	</a>
	<span>{offset + 1} - {Math.min(offset + limit, count)} of {count}</span>
	<a href="?limit={limit}&offset={offset + limit}">
		<button disabled={offset + limit > count}
						aria-label="right arrow icon"
						aria-describedby="next">
			<span class="material-symbols-outlined">arrow_forward</span>
		</button>
	</a>
</div>
