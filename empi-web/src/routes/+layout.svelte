<script lang="ts">
	import '@fontsource/source-sans-pro';
	import '$lib/styles/styles.css';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Login from '$lib/components/Login.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';

	import MaterialSymbolsKeyboardArrowRight from 'virtual:icons/material-symbols/keyboard-arrow-right';
	import { base, resolve } from '$app/paths';
	import { invalidateAll } from '$app/navigation';
	import { ENABLE_ATTRS } from '$lib/constants';
	import type { Snippet } from 'svelte';
	import { getCurrentAcademicYear, getCurrentSemesterUI } from '$lib/settings';
	import VerticalSeparator from '$lib/components/visual/VerticalSeparator.svelte';

	let { children, data }: { children: Snippet, data: LayoutServerData } = $props();
	const settings = data.settings;

	async function switchLocale() {
		const currentLocale = data.locale;
		let newLocale;
		if (currentLocale === 'sk') {
			newLocale = 'en';
		}
		else {
			newLocale = 'sk';
		}
		await cookieStore.set('locale', newLocale);
		document.getElementsByTagName('html').item(0)?.setAttribute('lang', newLocale);
		invalidateAll();
	}
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
			<div>{$t('common.academic_year')}&nbsp;<strong>{getCurrentAcademicYear(settings)}</strong></div>
			<VerticalSeparator></VerticalSeparator>
			<div style="width: fit-content">{$t(getCurrentSemesterUI(settings))}</div>
		</div>
	</div>
	<nav>
		<a href="{base}/">{$t('common.home')}</a>
		<a href="{resolve('/guide')}">{$t('common.guide')}</a>
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
			{#if data.user?.is_staff}
				<Dropdown title={$t('common.administration')}>
					{#if ENABLE_ATTRS}
						<div><a href="{base}/attributes">{$t('common.attributes')}</a></div>
					{/if}
					<div><a href="{base}/admin/research-list">{$t('common.research_list')}</a></div>
					<div><a href="{base}/admin/student-points">{$t('common.student_points')}</a></div>
					<div><a href="{base}/admin/add-admin">{$t('common.add_admin')}</a></div>
					<div><a href="{base}/admin/password-reset">{$t('common.password_reset')}</a></div>
				</Dropdown>
			{/if}
			<div id="language-switch">
				<button type="button" onclick={switchLocale}><span
					class={{'font-light': data.locale === 'en'}}>Slovenčina</span><span class="font-light"> | </span><span
					class={{'font-light': data.locale === 'sk'}}>English</span></button>
			</div>
			<ThemeToggle></ThemeToggle>
		</div>
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

<style>
	@media screen and (min-width: 1200px) {
		#language-switch {
			position: absolute;
			right: 1em;
		}
	}
</style>
