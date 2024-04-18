<script lang="ts">
	import { t } from '$lib/translations';

	export let show: boolean;
	export let dismissible = true;

	let dialog: HTMLDialogElement;

	export const dismiss = () => {
		dialog.close();
	};

	$: if (dialog && show) {
		dialog.showModal();
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (show = false)}
	on:click|self={() => {if (dismissible) dialog.close()}}
	on:cancel={(e) => {if(!dismissible) e.preventDefault()}}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div on:click|stopPropagation>
		<slot name="header"></slot>
		<hr>
		<slot></slot>

		<!-- svelte-ignore a11y-autofocus -->
		{#if dismissible}
			<hr>
			<button autofocus on:click={() => dialog.close()}>{$t('common.close')}</button>
		{/if}
	</div>
</dialog>

<style>
    dialog {
        max-width: 32em;
        border-radius: 0.2em;
        border: none;
    }

    dialog::backdrop {
        background: rgba(0, 0, 0, 0.3);
    }

    dialog[open] {
        animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    @keyframes zoom {
        from {
            transform: scale(0.95);
        }
        to {
            transform: scale(1);
        }
    }

    dialog[open]::backdrop {
        animation: fade 0.2s ease-out;
    }

    @keyframes fade {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>
