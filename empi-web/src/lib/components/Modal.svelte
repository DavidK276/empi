<script lang="ts">
	import { t } from '$lib/translations';
	import type { Snippet } from "svelte";

	let { show = $bindable(), hasCloseButton = true, dismissible = true, header, children }: {
		show: boolean,
		hasCloseButton: boolean,
		dismissible: boolean,
		header: Snippet,
		children: Snippet
	} = $props();

	let dialog: HTMLDialogElement;

	$effect(() => {
		if (dialog && show) {
			dialog.showModal();
		}
		else if (!show) {
			dialog.close();
		}
	});
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
<dialog bind:this={dialog} oncancel={(e) => {if(!dismissible) e.preventDefault()}}
        onclick={() => {if (dismissible) dialog.close()}} onclose={() => (show = false)}>
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div onclick={(e) => e.stopPropagation()}>
		{@render header?.()}
		<hr>
		{@render children?.()}

		<!-- svelte-ignore a11y_autofocus -->
		{#if dismissible && hasCloseButton}
			<hr>
			<button autofocus onclick={() => dialog.close()}>{$t('common.close')}</button>
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
