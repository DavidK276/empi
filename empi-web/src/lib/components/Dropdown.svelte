<script lang="ts">
	import { col, dropdown, dropdownContent } from '$lib/style.css';

	const toggleDropdown = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		const toggledDropdown = target.parentElement;
		if (toggledDropdown != null) {
			toggledDropdown.classList.toggle('show');

			const dropdowns = document.getElementsByClassName(dropdown);
			for (const dropdown of dropdowns) {
				if (dropdown !== toggledDropdown) {
					dropdown.classList.remove('show');
				}
			}
		}
	};

	export let title: string;
</script>

<div class="{dropdown}">
	<button on:click={toggleDropdown}>
		{title}
		<span class="material-symbols-outlined" style="pointer-events: none">expand_more</span>
	</button>
	<div class="{dropdownContent} {col}">
		<slot></slot>
	</div>
</div>