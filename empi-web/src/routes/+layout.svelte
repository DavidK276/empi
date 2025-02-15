<script lang="ts">
	import '@fontsource/source-sans-pro';
	import '$lib/styles/styles.css';

	import { getSetting } from '$lib/functions';
	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Login from '$lib/components/Login.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';

	import MaterialSymbolsKeyboardArrowRight from 'virtual:icons/material-symbols/keyboard-arrow-right';
	import { base } from '$app/paths';
	import { ENABLE_ATTRS } from '$lib/constants';
	import type { Snippet } from "svelte";
	import { getCurrentSemesterUI } from "$lib/settings";
	import VerticalSeparator from "$lib/components/visual/VerticalSeparator.svelte";

	let { children, data }: { children: Snippet, data: LayoutServerData } = $props();
	const settings = data.settings;
</script>

<div aria-hidden="true" class="row unsupported-browser">
	<div class="col hor-center" style="width: 100%; align-items: center">
		<p>Používate zastaranú verziu prehliadača alebo nepodporovaný prehliadač. Na stránke sa môžu vyskytnúť vizuálne
			chyby.</p>
		<p>Odporúčame použiť aktuálnu verziu podporovaných prehliadačov: Chrome, Firefox</p>
	</div>
</div>
<header class="row m-col hor-center ver-center">
	<div class="row ver-center">
		<div class="hor-center row"
		     style="border: 2px var(--button-primary) solid; border-radius: var(--sm); padding: var(--sm) var(--md); gap: var(--sm)">
			<div>Akademický
				rok&nbsp;<strong>{getSetting(settings, "CURRENT_ACAD_YEAR")}</strong></div>
			<VerticalSeparator></VerticalSeparator>
			<div style="width: fit-content">{getCurrentSemesterUI(settings)} semester</div>
		</div>
	</div>
	<nav>
		<a href="{base}/">{$t('common.home')}</a>
		<a href="{base}/guide">{$t('common.guide')}</a>
		{#if data.user?.is_staff}
			<a href="{base}/research">{$t('common.create_research')}</a>
		{/if}
	</nav>
	<div class="row m-col ver-center">
		<div class="row ver-center">
			{#if data.user != null}
				<Dropdown title={(data.user.first_name + ' ' + data.user.last_name).trim() || $t('common.account')}>
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
					<div>
						<a href="{base}/account">{$t('common.account')}
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
			{#if !data.user?.is_staff}
				<ThemeToggle></ThemeToggle>
			{/if}
		</div>
		{#if data.user?.is_staff}
			<div class="row ver-center">
				<Dropdown title={$t('common.administration')}>
					{#if ENABLE_ATTRS}
						<div><a href="{base}/attributes">{$t('common.attributes')}</a></div>
					{/if}
					<div><a href="{base}/admin/research-list">{$t('common.research_list')}</a></div>
					<div><a href="{base}/admin/student-points">{$t('common.student_points')}</a></div>
					<div><a href="{base}/admin/add-admin">{$t('common.add_admin')}</a></div>
					<div><a href="{base}/admin/password-reset">{$t('common.password_reset')}</a></div>
				</Dropdown>
				<ThemeToggle></ThemeToggle>
			</div>
		{/if}
	</div>
</header>
<div class="row ver-top hor-center">
	<div class="content">
		{@render children?.()}
	</div>
</div>
<footer class="row ver-center hor-center">
	<div>
		<p style="text-align: center">{$t('common.author_text')}</p>
	</div>
</footer>
