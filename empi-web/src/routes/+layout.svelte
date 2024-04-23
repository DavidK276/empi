<script lang="ts">
	import '@fontsource/source-sans-pro';
	import { content, row } from '$lib/style.css';
	import { themeClass, vars } from '$lib/theme.css';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Login from '$lib/components/Login.svelte';

	export let data: LayoutServerData;
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
					<div><a href="/account/points">{$t('common.my_points')}<span
						class="material-symbols-outlined">navigate_next</span></a>
					</div>
				{/if}
				<div><a href="/account">{$t('common.account')}<span class="material-symbols-outlined">navigate_next</span></a>
				</div>
				<Login is_logged_in="{true}"></Login>
			</Dropdown>
		{:else}
			<a href="/research">
				{$t('common.create_research')}
			</a>
			<Dropdown title="{$t('common.account')}">
				<Login is_logged_in="{false}"></Login>
			</Dropdown>
		{/if}
		{#if data.user?.is_staff}
			<Dropdown title="{$t('common.administration')}">
				<div><a href="/attributes">{$t('common.attributes')}</a></div>
				<div><a href="/admin/research-points">{$t('common.research_points')}</a></div>
				<div><a href="/admin/student-points">{$t('common.student_points')}</a></div>
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
