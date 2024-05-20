<script lang="ts">
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import MaterialSymbolsWarningOutline from 'virtual:icons/material-symbols/warning-outline';


	export let forId: string;
	export let labelText: string;
	export let hintText: string;
	export let icon: 'info' | 'warning';

	let hintVisible: boolean = false;
</script>

<div style="display: flex;" class="my-label">
	<label for={forId} style="display: inline-flex"
				 on:mouseenter={() => hintVisible = true}
				 on:mouseleave={() => hintVisible = false}>
		{labelText}
		{#if icon === 'info'}
			<MaterialSymbolsInfoOutline width="24px" height="24px"></MaterialSymbolsInfoOutline>
		{:else if icon === 'warning'}
			<MaterialSymbolsWarningOutline width="24px" height="24px"></MaterialSymbolsWarningOutline>
		{/if}
	</label>
	<div class="hint-parent" style:visibility={hintVisible ? 'visible' : 'hidden'}>
		<div class="arrow" style="margin-left: var(--sm)"></div>
		<div class="hint" id="username-hint">{hintText}</div>
	</div>
</div>

<style>
    :root {
        --arrow-size: 1.5rem;
    }

    .hint-parent {
        visibility: hidden;
        display: flex;
    }

    @media screen and (max-width: 767px) {
        .hint-parent {
            visibility: visible;
        }
    }

    .hint {
        align-items: center;
        border: 2px solid var(--text-primary);
        border-left: none;
        border-radius: var(--xs);
        padding: var(--sm);
        display: inline-block;
        color: light-dark(#fff, #000);
        background-color: var(--background-secondary);
    }

    .arrow::before {
        --height: calc(var(--arrow-size) / 2 * 3);

        content: '';
        position: relative;
        right: 0;
        top: calc(50% - var(--height) / 2);
        width: var(--arrow-size);
        height: var(--height);

        clip-path: polygon(0 50%, 100% 12.5%, 100% 87.5%);
        background-color: var(--background-secondary);
        display: inline-flex;
    }
</style>