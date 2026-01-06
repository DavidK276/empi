<script lang="ts">
	import { slide } from "svelte/transition";
	import { onMount } from "svelte";

	let { email = null }: { email?: string | null } = $props();
	let shown = $state(false);

	onMount(() => shown = true);
</script>

{#if shown}
	<div class="row ver-center" style="margin: var(--sm) 0" transition:slide={{duration: 100}}>
		{#if email == null}
			<input type="email" class="email-input">
		{:else}
			<input type="email" class="email-input" value={email}>
		{/if}
		<button onclick={() => shown = false} style="background-color: var(--danger)"
		        type="button">-
		</button>
	</div>
{/if}
