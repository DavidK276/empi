<script lang="ts">
    import type { PageData } from './$types';

    export let data: PageData;
</script>

<h1>Welcome to SvelteKit</h1>
{#if data.user !== undefined && data.user.first_name !== undefined}
    <p>Vitajte, {data.user.first_name} {data.user.last_name}</p>
{/if}
