<script lang="ts">
	function deleteOption(e: Event) {
		const removeButton = e.target as HTMLButtonElement;
		const parent = removeButton.parentElement;
		if (parent != null) {
			parent.remove();
		}
	}

	export let value: string | null;
</script>

<label class="row ver-top" style="margin: var(--sm) 0">
	{#if value}
		<input type="text" name="values[]" {value} readonly>
	{:else}
		<input type="text" name="values[]">
	{/if}
	<button type="button" style="background-color: var(--danger); margin: 0" on:click={deleteOption}>-</button>
</label>

<style>
	input {
			margin: 0;
	}
</style>