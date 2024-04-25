<script lang="ts">
	import { row } from '$lib/style.css';
	import { vars } from '$lib/theme.css';

	function deleteOption(e: Event) {
		const removeButton = e.target as HTMLButtonElement;
		const parent = removeButton.parentElement;
		if (parent != null) {
			parent.remove();
		}
	}

	export let value: string | null;
</script>

<label class="{row} ver-top" style="margin: {vars.sm} 0">
	{#if value}
		<input type="text" name="values[]" value={value} style="margin: 0" readonly>
	{:else}
		<input type="text" name="values[]" style="margin: 0">
	{/if}
	<button type="button" style="background-color: {vars.danger}; margin: 0" on:click={deleteOption}>-</button>
</label>