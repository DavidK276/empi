<script lang="ts">

	export let open: boolean;
	export let title: string;
</script>

<details open={open}>
	<summary>{title}</summary>
	<div>
		<slot></slot>
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