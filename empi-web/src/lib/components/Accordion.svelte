<script lang="ts">

</script>
<div class="accordion">
	<slot></slot>
</div>

<style>
    .accordion {
        border: 1px solid var(--button-primary);
        border-radius: var(--xs);
        overflow: hidden;
    }
</style>