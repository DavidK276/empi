<script lang="ts">
	import 'material-symbols';
	import '@fontsource/source-sans-pro';
	import { container, dropdown, dropdownContent } from '$lib/style.css';
	import { themeClass, vars } from '$lib/theme.css';

	import { t } from '$lib/translations';
	import type { LayoutData } from './$types';
	import { toggleDropdown } from '$lib/functions';

	export let data: LayoutData;
</script>

<div class="{themeClass}">
	<header class="{container} hor-center ver-center">
		<nav>
			<a href="/">{$t('common.home')}</a>
			<a href="/about">{$t('common.about')}</a>
		</nav>
		{#if data.user != null}
			<div class="{dropdown}">
				<button>
					{data.user.first_name} {data.user.last_name}
					<span class="material-symbols-outlined">expand_more</span>
				</button>
				<div class="{dropdownContent}">
					<form method="POST" action="?/logout">
						<button type="submit" name="submit">{$t('common.logout')}</button>
					</form>
				</div>
			</div>
		{:else}
			<div class="{dropdown}">
				<button on:click={toggleDropdown}>
					{$t('common.account')}
					<span class="material-symbols-outlined" style="pointer-events: none">expand_more</span>
				</button>
				<div class="{dropdownContent}">
					<form method="POST" action="?/login">
						<label for="username">{$t('common.username')}: </label>
						<input type="text" id="username" name="username" required>
						<label for="password">{$t('common.password')}: </label>
						<input type="password" id="password" name="password" required>
						<button type="submit" name="submit" style="margin: {vars.sm} 0">{$t('common.login')}</button>
						<a href="/register">{$t('common.registration')}</a>
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
