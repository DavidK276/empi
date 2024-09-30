<script lang="ts">
	import MaterialSymbolsArrowForward from 'virtual:icons/material-symbols/arrow-forward';
	import register from '$lib/assets/screens/register.png';
</script>

<h1>Registrácia študenta</h1>
<figure>
	<img src="{register}" alt="Formulár s textovými poľami: Email, Meno, Priezvisko, Heslo, Heslo (znovu)">
	<figcaption>Obrazovka registrácie študenta</figcaption>
</figure>

<p>Pri registrácii je potrebné zadať údaje:</p>
<ul>
	<li><strong>Email:</strong> Slúži na kontakt so študentom, bude naň dostávať systémové emaily. Odporúčame použiť univerzitnú emailovú adresu.</li>
	<li><strong>Meno a priezvisko:</strong> Slúži na sledovanie študentových účastí vyučujúcim. Nie je zdieľané s nikým iným.</li>
	<li><strong>Heslo:</strong> Slúži na šifrovanie študentových účastí na výskumoch.</li>
</ul>

<a href="/account/register" style="font-size: 32px">Zoberte ma tam!<MaterialSymbolsArrowForward width="48px" height="48px"></MaterialSymbolsArrowForward></a>

<style>
	img {
			max-width: 100%;
			box-shadow: 2px 2px 4px 0 light-dark(#000, #fff);
	}
	figcaption {
			text-align: center;
	}
</style>