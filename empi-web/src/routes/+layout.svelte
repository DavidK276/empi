<script lang="ts">
    import type { LayoutData } from './$types';

    export let data: LayoutData;
</script>

<header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        {#if data.user != null}
            <form method="POST" action="?/logout">
                <button type="submit" name="submit">Log out</button>
            </form>
        {:else}
            <form method="POST" action="?/login">
                <label for="username">Username: </label>
                <input type="text" id="username" name="username" required>
                <label for="password">Password: </label>
                <input type="password" id="password" name="password" required>
                <button type="submit" name="submit">Log in</button>
            </form>
        {/if}
    </nav>
</header>
<slot></slot>
<footer>
    <p>footer</p>
</footer>
