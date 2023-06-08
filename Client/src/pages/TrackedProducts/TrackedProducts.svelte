<script>
    import TrackProduct from "./page-components/TrackProduct.svelte";
    import TrackedProductsContainer from "./page-components/TrackedProductsContainer.svelte";
</script>

<main id="tracked-products-page">
    <div id="track-new-product-wrapper">
        <TrackProduct />
    </div>
    <div id="tracked-products-wrapper">
        <TrackedProductsContainer />
    </div>
</main>

<style>
</style>