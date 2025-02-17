<script lang="ts">
	import { t } from '$lib/translations';
	import MaterialSymbolsHelpOutline from 'virtual:icons/material-symbols/error-outline';
	import { base } from "$app/paths";
</script>

<div class="row ver-center" style="display: flex; margin: var(--lg) 0">
	<MaterialSymbolsHelpOutline height="24" width="24"></MaterialSymbolsHelpOutline>&nbsp;{$t('research.cancel_success')}
</div>
<button><a href="{base}/">{$t('common.goto_home')}</a></button>