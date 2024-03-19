<script lang="ts">
    import type { ActionData } from './$types';

    export let form: ActionData;
</script>
{#if form?.success === true}
    <p>Prihlásenie bolo úspešné!</p>
{:else if form?.success === false} <!-- this has to be explicitly compared to false so that the comparison is not true if form is undefined -->
    <p>Nepodarilo sa prihlásiť</p>
{/if}
<form method="POST">
    <label for="username">Username: </label>
    <input type="text" id="username" name="username" required>
    <label for="password">Password: </label>
    <input type="password" id="password" name="password" required>
    <button type="submit" name="submit">Log in</button>
</form>
