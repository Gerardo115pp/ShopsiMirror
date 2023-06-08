<script>
    import CustomQueryCreator from "./site-components/CustomQueryCreator.svelte";
    import { newNotification } from "../../components/notifications/events";
    import { GetMatchingProductsRequest, GetProductCompetitorsRequest } from "../../libs/HttpRequests";
    import SkuItemSearch from "./site-components/SkuItemSearch.svelte";
    import SavedQuerys from "./site-components/SavedQuerys.svelte";
    import bonhart_storage from "../../libs/bonhart-storage";


    let competitors = new Set();
    let current_product =   {};
    
    $: if (current_product?.product_id) {
        competitors = getCompetitors(current_product.product_id);
    }

    function getCompetitors(product_id) {
        const get_competitors_request = new GetProductCompetitorsRequest(bonhart_storage.Token);
        get_competitors_request.product_id = product_id;

        const on_success = response => {
            competitors = new Set(response.map(c => c.meli_id));
            console.log(competitors);

        }

        const on_error = error => {
            console.log(error);
            competitors = new Set();
        }
        
        get_competitors_request.do(on_success, on_error);
    }

    const currency_formatter = new Intl.NumberFormat("es-MX", {
        style: "currency",
        currency: "MXN",
        minimumFractionDigits: 2,
        maximumFractionDigits: 3
    });

</script>

<main id="product-position-page">
    <div id="ppp-product-data-wrapper">
        <div id="ppp-pdw-image-wrapper">
            {#if current_product.secure_thumbnail !== undefined}
                <img src="{current_product.secure_thumbnail}" alt="{current_product.name}"/>
            {/if}
        </div>
        <div id="ppp-pdw-pd-product-name">
            <h2 class="page-title">
                {current_product.name ? current_product.name : "No hay producto seleccionado"}
            </h2>
        </div>
        <div id="ppp-pdw-product-data">
            <div class="ppp-pdw-pda-attribute">
                <span class="ppp-pdw-pdaa-label">status</span>
                <span class="ppp-pdw-pdaa-value">{current_product.sku ? current_product.status : "No hay producto seleccionado"}</span>
            </div>
            <div class="ppp-pdw-pda-attribute">
                <span class="ppp-pdw-pdaa-label">Precio</span>
                <span class="ppp-pdw-pdaa-value">{current_product.initial_price ? currency_formatter.format(current_product.initial_price) : "No hay producto seleccionado"}</span>
            </div>
        </div>
    </div>
    <div id="ppp-product-sku-wrapper">
        <SkuItemSearch bind:current_product={current_product}/>
    </div>
    <div id="ppp-product-search-query-creator">
        <CustomQueryCreator target_product={current_product}/>
    </div>
    <div id="ppp-saved-search-querys">
        <SavedQuerys {competitors} our_product_meli_id={current_product.meli_id} current_sku={current_product.sku}/>
    </div>
</main>

<style>
    #product-position-page {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        row-gap: var(--spacing-3);
    }

    /* #product-position-page * {
        border: 1px solid red;
    } */

    /* Product data */

    #ppp-product-data-wrapper {
        width: 100%;
        grid-column: 1 / 7;
        display: grid;
        height: 19.34vh;
        grid-template: repeat(3, 1fr) / repeat(6, 1fr);
        grid-template-areas:
            'pi pi pt pt pt pt'
            'pi pi pd pd pd pd'
            'pi pi pd pd pd pd';
        /* pi=product image, pt=product title, pd=product data */
        /* padding: var(--spacing-2) var(--spacing-1); */
    }

    #ppp-pdw-image-wrapper {
        grid-area: pi;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    #ppp-pdw-image-wrapper img {
        width: 30%;
        object-fit: cover;
    }

    #ppp-pdw-product-data {
        grid-area: pd;
    }

    .ppp-pdw-pda-attribute {
        margin: var(--spacing-1) 0 0 0;
    }

    .ppp-pdw-pdaa-label {
        color: var(--dark-light-color);
        text-transform: uppercase;
    }

    .ppp-pdw-pdaa-label::after {
        content: ": ";
    }

    .ppp-pdw-pdaa-value {
        color: var(--primary-color);
    }

    #ppp-pdw-pd-product-name {
        grid-area: pt;
    }


    /* Product Sku  */

    #ppp-product-sku-wrapper {
        grid-column: 1 / 3;
    }

    #ppp-product-search-query-creator {
        grid-column: 3 / 7;
    }

    #ppp-saved-search-querys {
        grid-column: 1 / 7;
    }
</style>