<script lang="ts">
	import { t } from '$lib/translations.js';
	import Icon from "@iconify/svelte";
</script>

<p class="message" style="display: flex; margin: var(--lg) 0">
	<Icon icon="material-symbols:help-outline" width="24" height="24"></Icon>&nbsp;{$t('research.cancel_success')}</p>
<button><a href="/">{$t('common.goto_home')}</a></button>