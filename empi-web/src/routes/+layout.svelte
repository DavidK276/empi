<script lang="ts">
	import '@fontsource/source-sans-pro';

	import { t } from '$lib/translations';
	import type { LayoutServerData } from './$types';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Login from '$lib/components/Login.svelte';
	import Icon from "@iconify/svelte";

	export let data: LayoutServerData;
</script>

<header class="container row hor-center ver-center m-col">
	<nav>
		<a href="/">{$t('common.home')}</a>
		<a href="/about">{$t('common.about')}</a>
		{#if data.user == null}
			<a href="/research">{$t('common.create_research')}</a>
		{/if}
	</nav>
	{#if data.user != null}
		<Dropdown title="{data.user.first_name + ' ' + data.user.last_name}">
			{#if !data.user.is_staff}
				<div><a href="/attributes">{$t('common.attributes')}
					<Icon icon="material-symbols:keyboard-arrow-right" width="24" height="24"></Icon>
				</a></div>
				<div><a href="/account/points">{$t('common.my_points')}
					<Icon icon="material-symbols:keyboard-arrow-right" width="24" height="24"></Icon>
				</a>
				</div>
			{/if}
			<div><a href="/account">{$t('common.account')}
				<Icon icon="material-symbols:keyboard-arrow-right" width="24" height="24"></Icon>
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
			<div><a href="/attributes">{$t('common.attributes')}</a></div>
			<div><a href="/admin/research-points">{$t('common.research_points')}</a></div>
			<div><a href="/admin/student-points">{$t('common.student_points')}</a></div>
		</Dropdown>
	{/if}
</header>
<div class="container row ver-top hor-center">
	<div class="content">
		<slot></slot>
	</div>
</div>
<footer class="container row ver-center hor-center">
	<div>
		<p style="text-align: justify">{$t('common.author_text')}</p>
	</div>
</footer>
