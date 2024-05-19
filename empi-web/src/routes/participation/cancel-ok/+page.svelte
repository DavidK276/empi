<script lang="ts">
	import { t } from '$lib/translations.js';
	import { message } from "$lib/style.css";
</script>

<p class={message} style="display: flex; margin: var(--lg) 0"><span
		class="material-symbols-outlined">info</span>&nbsp;{$t('research.cancel_success')}</p>
<button style="padding: 0"><a href="/">{$t('common.goto_home')}</a></button>