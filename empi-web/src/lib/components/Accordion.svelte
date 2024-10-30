<script lang="ts">
	import type { Snippet } from "svelte";

	let { children }: { children: Snippet } = $props();
</script>

<div class="accordion">
	{@render children?.()}
</div>

<style>
    .accordion {
        border: 1px solid var(--button-primary);
        border-radius: var(--xs);
        overflow: hidden;
    }
</style>