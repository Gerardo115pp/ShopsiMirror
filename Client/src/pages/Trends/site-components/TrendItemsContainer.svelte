<script>
    import TrendItem from './TrendItem.svelte';

    export let items = [];
    export let our_product_meli_id = undefined;
    export let competitors = new Set();
</script>

<div id="trend-items-container">
    {#each items as item_data}
        <TrendItem is_ours={item_data.id === our_product_meli_id} is_competitor={competitors.has(item_data.id)} {item_data}/>
    {/each}
</div>

<style>
    #trend-items-container {
        overflow-y: auto;
        height: calc(100vh - var(--navbar-height) - 12vh);
    }
</style>