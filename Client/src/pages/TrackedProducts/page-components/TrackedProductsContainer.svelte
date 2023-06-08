<script>
    import { GetTrackedProducts, DeleteProductRequest, GetTrackedPerformanceRecords } from "../../../libs/HttpRequests";
    import bonhart_storage from '../../../libs/bonhart-storage';
    import { onMount, onDestroy } from "svelte";
    import { tracked_products_events, emitTrackProductsChanged } from '../events'

    let tracked_products = [];
    let tracked_products_prs = {}; // prs == performance records
    
    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 3
    });

    onMount(() => {
        getTrackedProducts();

        document.addEventListener(tracked_products_events.TRACKED_PRODUCTS_CHANGED, getTrackedProducts);
    });

    onDestroy(() => {
        document.removeEventListener(tracked_products_events.TRACKED_PRODUCTS_CHANGED, getTrackedProducts);
    });

    const getPerformanceRecords = () => {
        const get_prs_request = new GetTrackedPerformanceRecords(bonhart_storage.Token);

        const on_success = prs => {
            tracked_products_prs = prs.records;

            window.tracked_products_prs = prs; // TODO: Remove this. It's only for debugging purposes nothing is relying on this
        }

        const on_error = error => {
            console.log(error);
        }

        get_prs_request.do(on_success, on_error);
    }

    const getTrackedProducts = () => {
        const get_tracked_products_request = new GetTrackedProducts(bonhart_storage.Token);

        const on_success = products => {
            tracked_products = products;
            window.tracked_products = products; // TODO: Remove this. It's only for debugging purposes nothing is relying on this

            getPerformanceRecords();
        }

        const on_error = error => {
            console.log(error);
        }

        get_tracked_products_request.do(on_success, on_error);
    }

    const handleDeleteTrackedProduct = product_id => {
        if (product_id === undefined) {
            console.log("Programming error: product_id is undefined")
        }

        if (!confirm("¿Estás seguro de que quieres eliminar este producto de la lista de seguimiento?")) {
            return;
        }

        const delete_request = new DeleteProductRequest(bonhart_storage.Token);
        delete_request.product_id = product_id;

        const on_success = () => {
            emitTrackProductsChanged({product_id})
        }

        const on_error = error_code => {
            console.log(`Error code deleting tracked product: ${error_code}`);
        }

        delete_request.do(on_success, on_error);
    }

</script>

<div id="tpc-tracked-products-container">
    {#each tracked_products as tp}
        <div class="tracked-product">
            <div class="tp-product-attribute tp-product-image">
                <img src={tp.secure_thumbnail} alt={tp.name}/>
            </div>
            <div class="tp-product-attribute">
                <span class="tp-pa-label">SKU</span>
                <span class="tp-pa-value">{tp.sku}</span>
            </div>
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Estado</span>
                <span class="tp-pa-value">{tp.status}</span>
            </div>
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Nombre</span>
                <span class="tp-pa-value">{tp.name}</span>
            </div>
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Precio</span>
                <span class="tp-pa-value">{!isNaN(tracked_products_prs[tp.product_id]?.slice(-1)[0].current_price) ? price_formatter.format(tracked_products_prs[tp.product_id]?.slice(-1)[0].current_price ?? tp.initial_price) : price_formatter.format(tp.initial_price) }</span>
            </div>
            {#if tp.performance_record?.price_change !== undefined}
                <div class="tp-product-attribute">
                    <span class="tp-pa-label">D/precio</span>
                    <span class="tp-pa-value">{tp.performance_record.price_change ?? "?"}</span>
                </div>
            {/if}
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Ventas</span>
                <span class="tp-pa-value">{tracked_products_prs[tp.product_id]?.slice(-1)[0].sales ?? "?"}</span>
            </div>
            {#if tp.performance_record?.sales_change !== undefined}
                <div class="tp-product-attribute">
                    <span class="tp-pa-label">D/ventas</span>
                    <span class="tp-pa-value">{tp.performance_record.sales_change ?? "?"}</span>
                </div>
            {/if}
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Visitas</span>
                <span class="tp-pa-value">{tracked_products_prs[tp.product_id]?.slice(-1)[0].visits ?? "?"}</span>
            </div>
            {#if tp.performance_record?.visits_change !== undefined}
                <div class="tp-product-attribute">
                    <span class="tp-pa-label">D/visitas</span>
                    <span class="tp-pa-value">{tp.performance_record.visits_change ?? "?"}</span>
                </div>
            {/if}
            <div class="tp-product-attribute">
                <span class="tp-pa-label">Stock</span>
                <span class="tp-pa-value">{tracked_products_prs[tp.product_id]?.slice(-1)[0].stock ?? "?"}</span>
            </div>
            <div class="tp-product-attribute">
                <span class="tp-pa-label">ID</span>
                <span class="tp-pa-value">{tp.meli_id}</span>
            </div>
            <div class="tp-product-actions">
                <button on:click={() => handleDeleteTrackedProduct(tp.product_id)} class="danger-btn delete-product-action material-symbols-outlined">
                    delete
                </button>
            </div>
        </div>
    {/each}
</div>


<style>
    .tracked-product {
        --tp-box-width: 100%;

        display: flex;
        width: var(--tp-box-width);
        align-items: center;
        gap: var(--spacing-2);
        padding: var(--spacing-1);
        border: 1px solid var(--primary-color);
    }

    .tracked-product:first-of-type {
        border: none;
    }

    .tp-product-attribute.tp-product-image {
        width: calc(var(--spacing-3)*1.7);
        margin-right: var(--spacing-2);
    }
    /* Debug */
    /* .tracked-product * {
        border : 1px solid red;
    } */

    .tp-product-image img {
        width: 100%;
    }
    
    .tp-product-attribute {
        width: calc(var(--tp-box-width) / 9.5);
        font-size: calc(var(--font-size-small)*0.8);
    }

    .tp-pa-label {
        color: var(--primary-color);
    }

    .tp-pa-label::after {
        content: ":";
    }

    .tp-product-actions {
        display: flex;
        width: calc(var(--tp-box-width) / 7);
        justify-content: center;
        gap: var(--spacing-1);
    }
  

</style>
