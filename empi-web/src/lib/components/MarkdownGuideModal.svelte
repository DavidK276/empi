<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';

	let { show = $bindable(false) }: { show: boolean } = $props();
</script>

<Modal bind:show={show} dismissible={true} hasCloseButton={false}>
	{#snippet header()}
		<h2>Markdown návod</h2>
		<p>Vybrané prvky jazyka Markdown</p>
	{/snippet}
	<table>
		<tbody>
		<tr>
			<th>Markdown</th>
			<th>Výsledok</th>
		</tr>
		<tr>
			<td># Nadpis 1</td>
			<td><h1>Nadpis 1</h1></td>
		</tr>
		<tr>
			<td>## Nadpis 2</td>
			<td><h2>Nadpis 2</h2></td>
		</tr>
		<tr>
			<td>### Nadpis 3</td>
			<td><h3>Nadpis 3</h3></td>
		</tr>
		<tr>
			<td>*Šikmý text*</td>
			<td><i>Šikmý text</i></td>
		</tr>
		<tr>
			<td>**Tučný text**</td>
			<td><strong>Tučný text</strong></td>
		</tr>
		<tr>
			<td>[odkaz](https://www.example.com)</td>
			<td><a href="https://example.com">odkaz</a></td>
		</tr>
		</tbody>
	</table>
</Modal>

<style>
    table {
        width: 100%;
    }

    td {
        text-align: center;
    }

    h2 {
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>