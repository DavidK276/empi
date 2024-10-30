<script lang="ts">
	import { browser } from "$app/environment";

	let theme: string | null = (browser) ? localStorage.getItem("theme") : null;

	let themeSelect: HTMLSelectElement;
</script>

<button id="theme-toggle" onclick={() => {
						const selectedTheme = themeSelect.item((themeSelect.selectedIndex + 1) % 3)?.value || "os";
						themeSelect.value = selectedTheme;
						localStorage.setItem("theme", selectedTheme);
	        }}
        type="button">
	<select bind:this={themeSelect} id="theme-select">
		<option selected={theme === 'os'} value="os">OS</option>
		<option selected={theme === 'light'} value="light">Light</option>
		<option selected={theme === 'dark'} value="dark">Dark</option>
	</select>
</button>