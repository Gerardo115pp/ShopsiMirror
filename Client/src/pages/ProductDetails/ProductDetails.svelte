<script>
    import bonhart_storage, { standard_generic_stores } from "../../libs/bonhart-storage";
    import { GetProductCompetitorsRequest } from "../../libs/HttpRequests";
    import CompetitorRow from "./site-components/CompetitorRow.svelte";
    import { getThumbnailId } from  '../../libs/dandelion-utils';
    import { product_detail_events } from "./events";
    import { onMount, onDestroy } from 'svelte';
    import { push } from "svelte-spa-router";

    const selected_product = bonhart_storage.readGeneric(standard_generic_stores.PRODUCTS, 'selected_product');
    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    });

    onMount(() => {
        requestCompetitors();
        document.addEventListener(product_detail_events.DELETED_COMPETITOR, requestCompetitors);
    });

    onDestroy(() => {
        document.removeEventListener(product_detail_events.DELETED_COMPETITOR, requestCompetitors);
    });




    function requestCompetitors() {
        const competitors_request = new GetProductCompetitorsRequest(bonhart_storage.Token);
        competitors_request.product_id = selected_product.product.product_id;

        const on_success = response_data => {
            selected_product.competitors = response_data;
        }

        const on_error = http_error_code => {
            console.log(http_error_code);
        }

        competitors_request.do(on_success, on_error);
    }

    const getBiggerImage = thumbnail_url => {
        const thumbnail_id = getThumbnailId(thumbnail_url);
        return `https://http2.mlstatic.com/D_${thumbnail_id}-O.webp`;
    }
    
</script>

<div id="meli-product-details">
    <div id="mpd-product-details-wrapper">
        <div id="mpd-product-image">
            <img src={getBiggerImage(selected_product.product.secure_thumbnail)} alt={selected_product.product.name}/>
        </div>
        <div id="mpd-product-name-wrapper">
            <h2 class="page-title">
                <a href="{selected_product.product.meli_url}" alt="{selected_product.product.name}" target="_blank">
                    {selected_product.product.name}
                </a>
            </h2>
        </div>
        <div id="mpd-product-attributes">
            <div class="mpd-pa-wrapper">
                <span class="mpd-pa-label">SKU</span>
                <span class="mpd-pa-value">{selected_product.product.sku}</span>
            </div>
            <div class="mpd-pa-wrapper">
                <span class="mpd-pa-label">Estado</span>
                <span class="mpd-pa-value">{selected_product.product.status}</span>
            </div>
            <div class="mpd-pa-wrapper">
                <span class="mpd-pa-label">Precio</span>
                <span class="mpd-pa-value">{price_formatter.format(selected_product.product.initial_price)}</span>
            </div>
            <div class="mpd-pa-wrapper">
                <span class="mpd-pa-label">Condicion</span>
                <span class="mpd-pa-value">{selected_product.product.condition}</span>
            </div>
        </div>
        <div id="mdp-product-controls">
            <button on:click={() => push(`/trends/${selected_product.product.meli_id}`)} class="full-btn" id="mdp-pc-trends">
                Ver tendencias
            </button>
        </div>
    </div>
    <div id="mpd-product-competitors-container">
        {#if selected_product.competitors.length > 0}
            {#each selected_product.competitors as competitor}
                <CompetitorRow competitor_data={competitor} />
            {/each}
        {/if}
    </div>
</div>

<style>
    #meli-product-details {
        margin-top: var(--navbar-height);
    }

    /* #meli-product-details * {
        border: 1px solid red;
    } */

    #mpd-product-details-wrapper {
        display: grid;
        grid-template: repeat(6, 1fr) / repeat(9, 1fr);
        grid-gap: var(--spacing-1);
        grid-template-areas: 
            'i i i n n n n n n'
            'i i i v v v v v v'
            'i i i v v v v v v'
            'i i i v v v v v v'
            'i i i v v v v v v'
            'i i i c c c c c c';
        ;
        /* i=image, n=name, v=values, c=controls */
        padding: var(--spacing-2);
        border-bottom: 2px solid var(--primary-color);
    }

    #mpd-product-image {
        grid-area: i;
        display: grid;
        place-items: center;
    }

    #mpd-product-image img {
        width: clamp(10ch, 100%, 20vw);
        object-fit: contain;
    }

    #mpd-product-name-wrapper {
        display: flex;
        grid-area: n;
        align-items: center;
    }

    #mpd-product-name-wrapper h2 a {
        color: var(--primary-color);
        text-decoration: none;
    }

    /* Attributes */

    #mpd-product-attributes {
        display: flex;
        gap: var(--spacing-3);
        grid-area: v;
        padding: var(--spacing-3) 0 0 var(--spacing-2);
    }

    /* .mpd-pa-wrapper {
    } */

    .mpd-pa-label {
        color: var(--primary-color);
    }

    .mpd-pa-label::after {
        content: ':';
    }

    #mpd-product-competitors-container {
        max-height: calc(var(--spacing-h1)*.84);
        overflow-y: auto;
    }
</style>