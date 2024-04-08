<script lang="ts">
    import type { LayoutServerData } from './$types';

    export let data: LayoutServerData;
</script>

<h1>EMPI</h1>
<p>tu bude hlavná stránka</p>
{#if data.user != null }
    <p>Vitajte, {data.user.first_name} {data.user.last_name}</p>
{/if}
