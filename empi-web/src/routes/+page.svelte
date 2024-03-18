<script lang="ts">
    import type { PageData } from './$types';

    export let data: PageData;
</script>

<h1>Welcome to SvelteKit</h1>
{#if data.first_name !== undefined && data.last_name !== undefined}
    <p>{data.first_name} {data.last_name}</p>
{/if}
