<script lang="ts">

	import { accordionTab, accordionTabContent, accordionTabInput, accordionTabLabel } from '$lib/style.css';

	export let id: string;
	export let checked: boolean;
	export let title: string;
</script>
<div class="{accordionTab}">
	<input type="checkbox" name="research-accordion" id="{id}" class="{accordionTabInput}" checked="{checked}">
	<label for="{id}" class="{accordionTabLabel}">{title}
		<span class="material-symbols-outlined">expand_more</span>
	</label>
	<div class="{accordionTabContent}">
		<slot></slot>
	</div>
</div>