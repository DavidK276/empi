<script lang="ts">
	import 'material-symbols';
	import '@fontsource/source-sans-pro';
	import { container, dropdown, dropdownContent } from '$lib/style.css';
	import { themeClass, vars } from '$lib/theme.css';

	import type { LayoutData } from './$types';

	export let data: LayoutData;
</script>

<div class="{themeClass}">
	<header class="{container} hor-center ver-center">
		<nav>
			<a href="/">Home</a>
			<a href="/about">About</a>
		</nav>
		{#if data.user != null}
			<form method="POST" action="?/logout">
				<button type="submit" name="submit">Log in</button>
			</form>
		{:else}
			<div class="{dropdown}">
				<button>Log in<span class="material-symbols-outlined">expand_more</span></button>
				<div class="{dropdownContent}">
					<form method="POST" action="?/login">
						<label for="username">Username: </label>
						<input type="text" id="username" name="username" required>
						<label for="password">Password: </label>
						<input type="password" id="password" name="password" required>
						<button type="submit" name="submit" style="margin: {vars.sm} 0">Log in</button>
					</form>
				</div>
			</div>
		{/if}
	</header>
	<slot></slot>
	<footer>
		<p>footer</p>
	</footer>
</div>
