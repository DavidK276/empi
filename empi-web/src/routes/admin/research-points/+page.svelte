<script lang="ts">
	import Pagination from '$lib/components/Pagination.svelte';
	import { t } from '$lib/translations';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { enhance } from '$app/forms';
	import type { PageServerData } from './$types';
	import { box, content, row } from '$lib/style.css';

	onMount(() => {
		if (!$page.data.user?.is_staff) {
			goto('/', { replaceState: true });
		}
	});

	function resetTheButton(event: Event) {
		const target = event.target as HTMLInputElement;
		const parent = target.parentElement as HTMLDivElement;
		const submitButton = parent.children.namedItem('submit') as HTMLButtonElement | null;
		if (submitButton != null) {
			submitButton.innerText = $t('common.submit');
			submitButton.style['background-color'] = '';
		}
	}

	export let data: PageServerData;
</script>
<h1>{$t('common.points')}</h1>
{#each data.researches as research}
	<div class={box}>
		<form method="POST" use:enhance={({submitter}) => {
			return async ({result, update}) => {
				if (result.type === 'success' && submitter != null) {
					submitter.innerText = $t('common.saved');
					submitter.style['background-color'] = 'green';
				}
				await update({reset: false});
			};
		}}>
			<label for="points">{research.name}</label>
			<div class="{content} {row} ver-center">
				<input type="hidden" name="url" value={research.url}>
				<input type="number" step="1" name="points" value={research.points} required style="margin: 0"
							 on:input={resetTheButton}>
				<button type="submit" id="submit">{$t('common.submit')}</button>
			</div>
		</form>
	</div>
{/each}
<Pagination count={data.count}></Pagination>