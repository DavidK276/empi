<script lang="ts">
	import '@fontsource/source-sans-pro';
	import '$lib/styles/styles.css';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Login from '$lib/components/Login.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';

	import MaterialSymbolsKeyboardArrowRight from 'virtual:icons/material-symbols/keyboard-arrow-right';
	import { base } from '$app/paths';
	import { ENABLE_ATTRS } from '$lib/constants';

	export let data: LayoutServerData;
</script>

<header class="row hor-center ver-center m-col">
	<nav>
		<a href="{base}/">{$t('common.home')}</a>
		<a href="{base}/guide">{$t('common.guide')}</a>
		{#if data.user?.is_staff}
			<a href="{base}/research">{$t('common.create_research')}</a>
		{/if}
	</nav>
	<div class="row ver-center">
		{#if data.user != null}
			<Dropdown title="{(data.user.first_name + ' ' + data.user.last_name).trim() || $t('common.account')}">
				{#if !data.user.is_staff}
					{#if ENABLE_ATTRS}
						<div><a href="{base}/attributes">{$t('common.attributes')}
							<MaterialSymbolsKeyboardArrowRight width="24px" height="24px"></MaterialSymbolsKeyboardArrowRight>
						</a></div>
					{/if}
					<div><a href="{base}/account/points">{$t('common.my_points')}
						<MaterialSymbolsKeyboardArrowRight width="24px" height="24px"></MaterialSymbolsKeyboardArrowRight>
					</a>
					</div>
				{/if}
				<div><a href="{base}/account">{$t('common.account')}
					<MaterialSymbolsKeyboardArrowRight width="24px" height="24px"></MaterialSymbolsKeyboardArrowRight>
				</a>
				</div>
				<Login is_logged_in={true}></Login>
			</Dropdown>
		{:else}
			<Dropdown title={$t('common.account')}>
				<Login is_logged_in={false}></Login>
			</Dropdown>
		{/if}
		{#if data.user?.is_staff}
			<Dropdown title={$t('common.administration')}>
				{#if ENABLE_ATTRS}
					<div><a href="{base}/attributes">{$t('common.attributes')}</a></div>
				{/if}
				<div><a href="{base}/admin/add-admin">{$t('common.add_admin')}</a></div>
				<div><a href="{base}/admin/password-reset">{$t('common.password_reset')}</a></div>
				<div><a href="{base}/admin/research-points">{$t('common.research_points')}</a></div>
				<div><a href="{base}/admin/student-points">{$t('common.student_points')}</a></div>
			</Dropdown>
		{/if}
		<div style="border-left: 1px solid var(--text-primary); height: 2rem; display: inline"></div>
		<ThemeToggle></ThemeToggle>
	</div>
</header>
<div class="row ver-top hor-center">
	<div class="content">
		<slot></slot>
	</div>
</div>
<footer class="row ver-center hor-center">
	<div>
		<p style="text-align: justify">{$t('common.author_text')}</p>
	</div>
</footer>
