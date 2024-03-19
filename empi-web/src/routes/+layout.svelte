<script lang="ts">
    import type { LayoutData } from './$types';
    import { invalidateAll } from "$app/navigation";

    export let data: LayoutData;

    function logout() {
        fetch('/account/logout', {
			method: 'POST',
		}).then(() => invalidateAll());
    }

</script>

<header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        {#if data.user}
            <a href="/" on:click={logout}>Logout</a>
        {:else}
            <a href="account/login">Login</a>
        {/if}
    </nav>
</header>
<slot></slot>
<footer>
    <p>footer</p>
</footer>
