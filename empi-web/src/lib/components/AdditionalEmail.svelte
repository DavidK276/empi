<script lang="ts">
	import { row } from '$lib/style.css';
	import { vars } from '$lib/theme.css';

	let nodeRef: HTMLElement;
</script>

<div class="{row} ver-center" style="margin: {vars.sm} 0" bind:this={nodeRef}>
	<input type="email" class="email-input" style="margin: 0">
	<button type="button" style="background-color: {vars.danger}"
					on:click={() => nodeRef.parentNode?.removeChild(nodeRef)}>-
	</button>
</div>
