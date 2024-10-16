<script lang="ts">
	import MaterialSymbolsArrowForward from 'virtual:icons/material-symbols/arrow-forward';
	import { t } from '$lib/translations';
	import { base } from "$app/paths";
</script>

<h1>{$t('common.guide')}</h1>

<h2>Ako to funguje?</h2>
<p>
	<cite>Študenti si vyskúšajú kognitívne a psychologické experimenty z pozície participantov. Osobná účasť v
		jednotlivých výskumoch pomôže pri lepšom porozumení metodológie empirických vied.</cite>
</p>
<p>
	<cite>Výskumy budú
		prebiehať počas celého semestra, študenti si spomedzi výskumov budú môcť vybrať tie, ktorých sa
		zúčastnia.</cite>
</p>
<p>
	<cite>Na získanie hodnotenia musia študenti absolvovať určitý počet hodín účasti na
		empirických výskumoch, ktoré budú buď online, alebo v laboratóriu.</cite>
</p>

<p style="text-align: end">(úryvok z informačného listu predmetu Účasť na empirickom výskume)</p>

<h2>Na čo slúži táto stránka?</h2>
<ul>
	<li>Prihlasovanie na výskumy, odhlasovanie z výskumov</li>
	<li>Sledovanie výskumov, na ktoré som sa prihlásil</li>
	<li>Zistenie aktuálneho počtu absolvovaných hodín</li>
	<li>Overenie, či bola účasť na termíne potvrdená</li>
</ul>

<h2>Ako sa zaznamenáva moja účasť?</h2>
<p>Po registrácii do systému ti bude pridelený anonymný identifikátor. Svoj token môžeš zistiť kedykoľvek
	na stránke detailov účtu. <a
			href="/account">Zoberte ma tam!
		<MaterialSymbolsArrowForward width="24px" height="24px"></MaterialSymbolsArrowForward>
	</a></p>
<p>Po zúčastnení na výskume svoj anonymný identifikátor odovzdaj organizátorovi výskumu a on ti potvrdí tvoju účasť.</p>

<h2>Zvoľte scenár</h2>
<div class="grid-container">
	<button type="button" class="m-w-full"><a href="{base}/guide/student/register">Chcem sa registrovať do systému</a>
	</button>
	<button type="button" class="m-w-full"><a href="{base}/guide/student/password">Zabudol som svoje heslo</a></button>
	<button type="button" class="m-w-full"><a href="{base}/guide/student/signup">Chcem sa prihlásiť na výskum</a></button>
	<button type="button" class="m-w-full"><a href="{base}/guide/student/cancel">Chcem zrušiť svoju prihlášku na
		výskum</a>
	</button>
	<button type="button" class="m-w-full"><a href="{base}/guide/student/points">Chcem zistiť moju účasť</a></button>
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