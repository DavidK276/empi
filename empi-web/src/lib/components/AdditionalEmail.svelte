<script lang="ts">
	export let email: string | null = null;
	let nodeRef: HTMLElement;
</script>

<div class="container row ver-center" style="margin: var(--sm) 0" bind:this={nodeRef}>
	{#if email == null}
		<input type="email" class="email-input" style="margin: 0">
	{:else}
		<input type="email" class="email-input" style="margin: 0" value={email}>
	{/if}
	<button type="button" style="background-color: var(--danger)"
					on:click={() => nodeRef.parentNode?.removeChild(nodeRef)}>-
	</button>
</div>
