<script lang="ts">
	let { email = null }: { email: string | null } = $props();
	let nodeRef: HTMLElement;
</script>

<div bind:this={nodeRef} class="row ver-center" style="margin: var(--sm) 0">
	{#if email == null}
		<input type="email" class="email-input">
	{:else}
		<input type="email" class="email-input" value={email}>
	{/if}
	<button onclick={() => nodeRef.parentNode?.removeChild(nodeRef)} style="background-color: var(--danger)"
	        type="button">-
	</button>
</div>

<style>
    input {
        margin: 0;
    }
</style>
