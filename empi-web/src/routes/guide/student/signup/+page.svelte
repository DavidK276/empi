<script lang="ts">
	import MaterialSymbolsArrowForward from 'virtual:icons/material-symbols/arrow-forward';
	import researchUser from '$lib/assets/screens/research-user.png';
</script>

<h1>Prihlásenie na výskum</h1>
<figure>
	<img src="{researchUser}" alt="Stránka s detailami výskumu: popisom a termínmi">
	<figcaption>Stránka detailov výskumu</figcaption>
</figure>

<ol>
	<li>Prihlás sa do systému svojimi prihlasovacími údajmi.</li>
	<li>Na hlavnej stránke nájdeš zoznam výskumov, ktorých sa môžeš zúčastniť. Vyber si jeden z nich kliknutím na tlačidlo <cite>Detaily</cite>. <a
		href="/">Zoberte ma tam!
		<MaterialSymbolsArrowForward width="24px" height="24px"></MaterialSymbolsArrowForward>
	</a>
	</li>
	<li>Na stránke detailov výskumu (ktorej náhľad vidíš vyššie) uvidíš okrem iného aj výpis termínov výskumu. Vyber si vhodný termín a prihlás sa naň stlačením tlačidla <cite>Zúčastniť sa</cite>.</li>
	<li>V prípade prihlásenia na online termín sa pri ňom po prihlásení naň zobrazí odkaz na zúčastnenie výskumu.</li>
</ol>

<style>
	img {
			max-width: 100%;
			box-shadow: 2px 2px 4px 0 light-dark(#000, #fff);
	}
	figcaption {
			text-align: center;
	}
</style>