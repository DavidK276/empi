<script lang="ts">
	import type { PageData } from './$types';
	import PasswordRequiredModal from '$lib/components/PasswordRequiredModal.svelte';

	export let data: PageData;
</script>
<PasswordRequiredModal></PasswordRequiredModal>
<h1>{data.research?.name}</h1>