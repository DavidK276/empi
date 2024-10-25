<script lang="ts">
	import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
	import MaterialSymbolsWarningOutline from 'virtual:icons/material-symbols/warning-outline';

	let { forId, labelText, hintText, icon }: {
		forId: string,
		labelText: string,
		hintText: string,
		icon: 'info' | 'warning'
	} = $props();

	let hintVisible: boolean = $state(false);
</script>

<div class="my-label" style="display: flex;">
	<label for={forId} onmouseenter={() => hintVisible = true}
	       onmouseleave={() => hintVisible = false}
	       style="display: inline-flex; min-width: fit-content">
		{labelText}
		{#if icon === 'info'}
			<MaterialSymbolsInfoOutline width="24px" height="24px"></MaterialSymbolsInfoOutline>
		{:else if icon === 'warning'}
			<MaterialSymbolsWarningOutline width="24px" height="24px"></MaterialSymbolsWarningOutline>
		{/if}
	</label>
	<div class="hint-parent" class:hidden={!hintVisible}>
		<div class="arrow" style="margin-left: var(--sm)"></div>
		<div class="hint" id="username-hint">{hintText}</div>
	</div>
</div>

<style>
    :root {
        --arrow-size: 1.5rem;
    }

    .hint-parent {
        display: flex;
    }

    @media screen and (min-width: 768px) {
        .hidden {
            visibility: hidden;
        }
    }

    .hint {
        align-items: center;
        border: 3px solid var(--background-secondary);
        border-radius: 12px;
        padding: var(--xs);
        display: inline-block;
        color: var(--text-primary);
    }

    .arrow::before {
        --height: calc(var(--arrow-size));

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