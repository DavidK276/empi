<script lang="ts">
	import researchEdit from '$lib/assets/screens/research-edit.png';
</script>

<h1>Správa výskumu</h1>
<figure>
	<img src="{researchEdit}" alt="Rozsialhla stránka s veľkým počtom formulárov a položiek">
	<figcaption>Obrazovka správy výskumu</figcaption>
</figure>

<ul>
	<li>Pred publikovať výskumu je potrebné pridať aspon jeden termín.</li>
	<li>Pri každom termíne je uvedené, koľko osôb sa naň prihlásilo.</li>
	<li>Možné je pridať popis výskumu aj URL na stránku s informáciami o výskume.</li>
	<li>Na stránku úpravy výskumu môže pristupovať každý s jej URL. Je možné pridať dodatočnú ochranu nastavením hesla.</li>
	<li>V záložke <cite>Poslať email</cite> je možné poslať email osobám prihláseným na niektorý z termínov výskumu.</li>
	<li>V záložke <cite>Zápisnica účasti študentov</cite> sa potvrdzuje účasť študentov na výskume prostredníctvom ich identifikátora.</li>
</ul>

<style>
	img {
			max-width: 100%;
			box-shadow: 2px 2px 4px 0 light-dark(#000, #fff);
	}
	figcaption {
			text-align: center;
	}
	li {
			margin-bottom: var(--sm);
	}
</style>