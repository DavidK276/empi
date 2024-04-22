<script lang="ts">
	import '@fontsource/source-sans-pro';
	import { enhance } from '$app/forms';
	import { content, error, row } from '$lib/style.css';
	import { themeClass, vars } from '$lib/theme.css';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { store } from '$lib/stores';
	import Dropdown from '$lib/components/Dropdown.svelte';

	export let data: LayoutServerData;
	let logging_in = false;
	let logging_out = false;

	function setPasswordSession(event: Event) {
		const form = event.target as HTMLFormElement;
		const passwordInput = form.elements.namedItem('password') as HTMLInputElement;
		$store.password = passwordInput?.value;
	}

	function unsetPasswordSession() {
		$store.password = '';
	}
</script>

<div class="{themeClass}">
	<header class="{row} hor-center ver-center m-col">
		<nav>
			<a href="/" style="margin: 0 {vars.sm}">{$t('common.home')}</a>
			<a href="/about" style="margin: 0 {vars.sm}">{$t('common.about')}</a>
		</nav>
		{#if data.user != null}
			<Dropdown title="{data.user.first_name + ' ' + data.user.last_name}">
				{#if !data.user.is_staff}
					<div><a href="/attributes">{$t('common.attributes')}<span
						class="material-symbols-outlined">navigate_next</span></a></div>
				{/if}
				<div><a href="/account">{$t('common.account')}<span class="material-symbols-outlined">navigate_next</span></a>
				</div>
				<div><a href="/account/points">{$t('common.my_points')}<span
					class="material-symbols-outlined">navigate_next</span></a>
				</div>
				<form method="POST" action="/?/logout" on:submit={unsetPasswordSession}
							use:enhance={() => {
									logging_out = true;

									return async ({ update }) => {
										await update();
										await goto("/");
										logging_out = false;
									};
								}}>
					{#if logging_out}
						<button type="submit" disabled>{$t('common.logging_out')}</button>
					{:else}
						<button type="submit" name="submit">{$t('common.logout')}</button>
					{/if}
				</form>
			</Dropdown>
		{:else}
			<Dropdown title="{$t('common.account')}">
				<form method="POST" action="/?/login" style="width: 100%" on:submit={setPasswordSession}
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
						<p class="{error}" style="white-space: nowrap">{$t('common.wrong_login')}</p>
					{/if}
					<div style="display: flex; flex-wrap: nowrap">
						{#if logging_in}
							<button type="submit" disabled>{$t('common.logging_in')}</button>
						{:else}
							<button type="submit" name="submit">{$t('common.login')}</button>
						{/if}
						<a href="/register" style="margin: 0 {vars.sm}">{$t('common.registration')}</a>
					</div>
				</form>
			</Dropdown>
			<button>
				<a href="/research" style="color: {vars.textSecondary}">
					{$t('common.create_research')}
					<span class="material-symbols-outlined" style="pointer-events: none">navigate_next</span>
				</a>
			</button>
		{/if}
		{#if data.user?.is_staff}
			<Dropdown title="{$t('common.administration')}">
				<div><a href="/attributes">{$t('common.attributes')}</a></div>
				<div><a href="/admin/points">{$t('common.points')}</a></div>
			</Dropdown>
		{/if}
	</header>
	<div class="{row} ver-top hor-center">
		<div class="{content}">
			<slot></slot>
		</div>
	</div>
	<footer class="{row} ver-center hor-center">
		<div>
			<p style="text-align: justify">{$t('common.author_text')}</p>
		</div>
	</footer>
</div>
