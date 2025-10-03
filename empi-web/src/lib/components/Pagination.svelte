<script lang="ts">
    import { page } from '$app/state';
    import { PAGE_SIZE } from '$lib/constants';
    import MaterialSymbolsArrowBack from 'virtual:icons/material-symbols/arrow-back';
    import MaterialSymbolsArrowForward from 'virtual:icons/material-symbols/arrow-forward';
    import { goto } from "$app/navigation";
    import { t } from '$lib/translations';


    let { count }: { count: number } = $props();

    let limit = Number.parseInt(page.url.searchParams.get('limit')!) || PAGE_SIZE;
    let offset = $state(Number.parseInt(page.url.searchParams.get('offset')!) || 0);

    $effect(() => {
        let query = new URLSearchParams(page.url.searchParams.toString());
        if (limit.toString() === (query.get('limit') || PAGE_SIZE.toString())
            && offset.toString() === (query.get('offset') || "0")) {
            return;
        }
        query.set('limit', limit.toString());
        query.set('offset', offset.toString());

        goto(`?${query.toString()}`, { invalidateAll: true });
    });
</script>

{#if count > PAGE_SIZE || true}
    <div class="content row ver-center hor-center">
        <button disabled={offset - limit < 0}
                onclick={() => offset -= limit}
                aria-label="right arrow icon"
                aria-describedby="previous">
            <MaterialSymbolsArrowBack width="24" height="24"></MaterialSymbolsArrowBack>
        </button>
        <span>{offset + 1} - {Math.min(offset + limit, count)} {$t('common.of')} {count}</span>
        <button disabled={offset + limit >= count}
                onclick={() => offset += limit}
                aria-label="right arrow icon"
                aria-describedby="next">
            <MaterialSymbolsArrowForward width="24" height="24"></MaterialSymbolsArrowForward>
        </button>
    </div>
{/if}
