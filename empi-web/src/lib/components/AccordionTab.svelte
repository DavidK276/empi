<script lang="ts">

	import type { Snippet } from "svelte";

	let { open, title, children }: { open: boolean, title: string, children: Snippet } = $props();

	const id = title.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/\s/, "-");
</script>

<div class="acc-tab">
	<div class="acc-title">
		<input checked={open} class="acc-checkbox" id="{id}-checkbox" type="checkbox">
		<label class="acc-label" for="{id}-checkbox">{title}</label>
	</div>
	<div class="acc-content-container">
		<div class="acc-content">
			{@render children?.()}
		</div>
	</div>
</div>

<style>
    .acc-checkbox {
        display: none;
    }

    .acc-label {
        cursor: pointer;
        display: inline-flex;
        align-items: center;

        &::before {
            content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M12.6 12L8 7.4L9.4 6l6 6l-6 6L8 16.6z'/%3E%3C/svg%3E");
            filter: var(--filter-white);
            width: 24px;
            height: 24px;
            display: inline-block;
            transition: rotate 200ms ease;
        }
    }

    .acc-title {
        background-color: var(--button-primary);
        color: var(--text-secondary);
        padding: var(--sm);

        &:has(input:checked) .acc-label::before {
            rotate: 90deg;
        }
    }

    .acc-content {
        padding: var(--sm);
    }

    .acc-content-container {
        height: 0;
        overflow: hidden;
        transition: height 200ms ease;
    }

    .acc-tab:has(.acc-title > input:checked) .acc-content-container {
        height: auto;
    }
</style>