<script lang="ts">
	import { t } from '$lib/translations';
	import { base } from "$app/paths";
</script>

<h1>{$t('common.guide')}</h1>

<h2>Na čo slúži táto stránka?</h2>
<p>Hlavnou úlohou tejto stránky je sprostredkovať študentom predmetu <cite>Účasť na empirickom výskume</cite> účasť na
	výskumoch.</p>
<p>Ako expert môžete na stránku pridať výskum, na ktorý sa budú prihlasovať predovšetkým študenti, ale aj verejnosť.</p>
<p>V prípade, že sa na výskum prihlásil študent, je pre účely predmetu <cite>Účasť na empirickom výskume</cite> potrebné
	potvrdiť jeho účasť.</p>


<h2>Zvoľte scenár</h2>
<div class="grid-container">
	<button type="button" class="m-w-full"><a href="{base}/guide/expert/create-research">Chcem pridať do systému nový
		výskum</a></button>
	<button type="button" class="m-w-full"><a href="{base}/guide/expert/edit-research">Chcem spravovať svoj výskum</a>
	</button>
</div>

<style>
    button {
        width: 100%;
    }

    .grid-container {
        display: grid;
        gap: var(--sm);
        grid-template-columns: auto auto auto;
    }

    @media screen and (max-width: 768px) {
        .grid-container {
            grid-template-columns: auto;
        }
    }
</style>