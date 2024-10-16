<script lang="ts">
	import { t } from '$lib/translations';
	import { base } from "$app/paths";
</script>

<h1>{$t('common.guide')}</h1>
<h2>Zvoľte scenár</h2>
<div class="grid-container">
	<button type="button" class="m-w-full"><a href="{base}/guide/student">Som študent predmetu Účasť na empirickom
		výskume</a>
	</button>
	<button type="button" class="m-w-full"><a href="{base}/guide/expert">Vykonávam výskum a chcem ho pridať do systému</a>
	</button>
	<!--	<button type="button" class="m-w-full"><a href="{base}/guide/public">Som návštevník</a></button>-->
</div>

<style>
    button {
        word-wrap: anywhere;
    }

    .grid-container {
        display: grid;
        gap: var(--sm);
        grid-template-columns: repeat(4, 50%);
    }

    @media screen and (max-width: 768px) {
        .grid-container {
            grid-template-columns: auto;
        }
    }
</style>