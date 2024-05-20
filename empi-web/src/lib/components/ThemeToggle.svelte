<script lang="ts">
	import { browser } from "$app/environment";

	let theme: string | null = null;

	if (browser) {
		theme = localStorage.getItem("theme");
	}

	let themeSelect: HTMLSelectElement;
</script>

<button type="button" id="theme-toggle"
        on:click={() => {
						const selectedTheme = themeSelect.item((themeSelect.selectedIndex + 1) % 3)?.value || "os";
						themeSelect.value = selectedTheme;
						localStorage.setItem("theme", selectedTheme);
	        }}>
	<select id="theme-select" bind:this={themeSelect}>
		<option value="os" selected={theme === 'os'}>OS</option>
		<option value="light" selected={theme === 'light'}>Light</option>
		<option value="dark" selected={theme === 'dark'}>Dark</option>
	</select>
</button>