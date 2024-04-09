<script lang="ts">
	import 'material-symbols';
	import '@fontsource/source-sans-pro';
	import { enhance } from '$app/forms';
	import { container, content, dropdown, dropdownContent, error } from '$lib/style.css';
	import { themeClass } from '$lib/theme.css';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import { page } from '$app/stores';
	import { toggleDropdown } from '$lib/functions';
	import { goto } from '$app/navigation';

	export let data: LayoutServerData;
	let logging_in = false;
	let logging_out = false;
</script>

<div class="{themeClass}">
	<header class="{container} hor-center ver-center">
		<nav>
			<a href="/">{$t('common.home')}</a>
			<a href="/about">{$t('common.about')}</a>
		</nav>
		{#if data.user != null}
			<div class="{dropdown}">
				<button on:click={toggleDropdown}>
					{data.user.first_name} {data.user.last_name}
					<span class="material-symbols-outlined">expand_more</span>
				</button>
				<div class="{dropdownContent}">
					<form method="POST" action="/?/logout"
								use:enhance={() => {
									logging_out = true;

									return async ({ update }) => {
										await update();
										await goto("/");
										logging_out = false;
									};
								}}>
						<a href="/account">{$t('common.account')}<span class="material-symbols-outlined">navigate_next</span></a>
						{#if logging_out}
							<button type="submit" disabled>{$t('common.logging_out')}</button>
						{:else}
							<button type="submit" name="submit">{$t('common.logout')}</button>
						{/if}
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
					<form method="POST" action="?/login" style="width: 100%"
								use:enhance={() => {
									logging_in = true;

									return async ({ update }) => {
										await update();
										logging_in = false;
									};
								}}>
						<label for="username">{$t('common.username')}: </label>
						<input type="text" id="username" name="username" required>
						<label for="password">{$t('common.password')}: </label>
						<input type="password" id="password" name="password" required minlength="4">
						{#if $page.form?.login === false}
							<p class="{error}">{$t('common.wrong_login')}</p>
						{/if}
						{#if logging_in}
							<button type="submit" disabled>{$t('common.logging_in')}</button>
						{:else}
							<button type="submit" name="submit">{$t('common.login')}</button>
						{/if}
						<a href="/register">{$t('common.registration')}</a>
					</form>
				</div>
			</div>
		{/if}
	</header>
	<div class="{container} ver-top hor-center">
		<div class="{content}">
			<slot></slot>
		</div>
	</div>
	<footer class="{container} ver-center hor-center">
		<div>
			<p>EMPI verzia 0.0.0. Pôvodne navrhol a vytvoril David Krchňavý v 2024 ako bakalársku prácu na Univerzite
				Komenského
				v Bratislave, Fakulta matematiky, fyziky a informatiky.</p>
		</div>
	</footer>
</div>
