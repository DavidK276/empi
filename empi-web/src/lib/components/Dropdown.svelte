<script lang="ts">
	import MaterialSymbolsKeyboardArrowRight from 'virtual:icons/material-symbols/keyboard-arrow-right';

	export let title: string;
	let isOpen = false;
</script>

<div class="dropdown" class:show={isOpen}>
	<button on:click={() => (isOpen = !isOpen)}>
		{title}
		<MaterialSymbolsKeyboardArrowRight icon="material-symbols:keyboard-arrow-down" width="24" height="24"></MaterialSymbolsKeyboardArrowRight>
	</button>
	<div class="dropdown-content col">
		<slot></slot>
	</div>
</div>

<style>
    .dropdown {
        display: inline-block;
    }

    @media screen and (min-width: 768px) {
        .dropdown {
            position: relative;
            float: left;
        }
    }

    .dropdown-content {
        display: none;
        position: absolute;
		    right: 0;
		    left: 0;
		    margin: 0 auto;
		    width: fit-content;
		    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.4);
		    background-color: var(--background-primary);
		    z-index: 1;
		    border-radius: var(--sm);
		    padding: var(--lg);
		    gap: var(--lg);
    }

    .dropdown:hover .dropdown-content, .dropdown.show .dropdown-content {
		    display: flex;
    }
</style>