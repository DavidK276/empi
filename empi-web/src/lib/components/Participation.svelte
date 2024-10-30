<script lang="ts">
	import type { Participation } from "$lib/objects/participation";

	let { participation }: { participation: Participation } = $props();
</script>
<div class="box" style="margin: 0; flex: 1 1 calc(33% - 1rem)">
	<form class="participation-form" style="display: flex; justify-content: center;">
		<button style="font-weight: 700; text-align: center">{participation.participant.token}</button>
		<input name="id" type="hidden" value={participation.id}>
		<input checked={participation.is_confirmed} name="is_confirmed" style="margin: 0 0 0 var(--sm)"
		       type="checkbox" value="true">
	</form>
</div>