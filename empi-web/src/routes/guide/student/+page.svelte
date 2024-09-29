<script lang="ts">
import { t } from "$lib/translations";
</script>

<h1>{$t('common.guide')}</h1>
<h2>Zvoľte scenár</h2>

<button type="button" class="m-w-full"><a href="/guide/student">Chcem sa registrovať do systému</a></button>
<button type="button" class="m-w-full"><a href="/guide/student">Chcem sa prihlásiť na výskum</a></button>
<button type="button" class="m-w-full"><a href="/guide/student">Chcem zrušiť svoju prihlášku na výskum</a></button>
<button type="button" class="m-w-full"><a href="/guide/student">Chcem zistiť stav mojich bodov</a></button>

<style>
	button {
			width: 33%;
			white-space: break-spaces;
			margin-bottom: var(--xs);
	}
</style>