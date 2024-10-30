<script lang="ts">
	function deleteOption(e: Event) {
		const removeButton = e.target as HTMLButtonElement;
		const parent = removeButton.parentElement;
		if (parent != null) {
			parent.remove();
		}
	}

	let { value }: { value: string | null } = $props();
</script>

<label class="row ver-top" style="margin: var(--sm) 0">
	{#if value}
		<input type="text" name="values[]" {value} readonly>
	{:else}
		<input type="text" name="values[]">
	{/if}
	<button onclick={deleteOption} style="background-color: var(--danger); margin: 0" type="button">-</button>
</label>

<style>
    input {
        margin: 0;
    }
</style>