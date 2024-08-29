<script lang="ts">
	import MaterialSymbolsKeyboardArrowDown from 'virtual:icons/material-symbols/keyboard-arrow-down';
	import MaterialSymbolsKeyboardArrowUp from 'virtual:icons/material-symbols/keyboard-arrow-up';

	export let title: string;
	let isOpen = false;
</script>

<div class="dropdown" class:show={isOpen}>
	<button on:click={() => (isOpen = !isOpen)}>
		{title}
		{#if isOpen}
			<MaterialSymbolsKeyboardArrowUp width="24" height="24"></MaterialSymbolsKeyboardArrowUp>
		{:else}
			<MaterialSymbolsKeyboardArrowDown width="24" height="24"></MaterialSymbolsKeyboardArrowDown>
		{/if}
	</button>
	<div class="dropdown-content col">
		<slot></slot>
	</div>
</div>

<style>
    .dropdown {
        display: inline-block;
    }

		button {
				cursor: pointer;
		}

    .dropdown-content {
        display: none;
        position: absolute;
        margin-inline: auto;
        width: fit-content;
        box-shadow: 0 8px 16px 0 var(--text-primary);
        background: var(--background-primary);
        z-index: 1;
        border-radius: var(--sm);
        padding: var(--lg);
        gap: var(--lg);
				margin-top: 2px;
    }

    @media screen and (min-width: 768px) {
        .dropdown {
            position: relative;
        }
    }

    @media screen and (max-width: 767px) {
        .dropdown-content {
            position: fixed;
            width: calc(100dvw - var(--xl));
            left: 0;
            right: 0;
        }
    }

    .dropdown.show .dropdown-content {
        display: flex;
    }
</style>