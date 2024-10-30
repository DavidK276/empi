<script lang="ts">

	import type { Snippet } from "svelte";

	let { open, title, children }: { open: boolean, title: string, children: Snippet } = $props();
</script>

<details {open}>
	<summary>{title}</summary>
	<div>
		{@render children?.()}
	</div>
</details>

<style>
    summary {
        cursor: pointer;
        background-color: var(--button-primary);
        color: var(--text-secondary);
        padding: var(--sm);
    }

    details > div {
        padding: var(--sm);
    }
</style>