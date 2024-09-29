<script lang="ts">
import { t } from "$lib/translations";
</script>

<h1>{$t('common.guide')}</h1>
<h2>Zvoľte scenár</h2>

<button type="button" class="m-w-full"><a href="/guide/student">Som študent predmetu Účasť na empirickom výskume</a></button>
<button type="button" class="m-w-full"><a href="/guide/expert">Vykonávam výskum a chcem ho pridať do systému</a></button>
<button type="button" class="m-w-full"><a href="/guide/public">Som návštevník</a></button>

<style>
	button {
			width: 33%;
			white-space: break-spaces;
			margin-bottom: var(--xs);
	}
</style>