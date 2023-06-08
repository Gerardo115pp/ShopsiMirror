<script>
    import { GetMeliItemData, PostTrackedProduct } from "../../../libs/HttpRequests";
    import { emitTrackProductsChanged, tracked_products_events } from '../events';
    import { newNotification } from '../../../components/notifications/events';
    import FieldData, { verifyFormFields } from "../../../libs/FieldData";
    import { getMeliIdFromUrl } from "../../../libs/dandelion-utils";
    import bonhart_storage from '../../../libs/bonhart-storage';
    import Input from "../../../components/Input/Input.svelte";
    import ProductPreview from './ProductPreview.svelte';
    import { onMount, onDestroy } from "svelte";

    let search_field = new FieldData("search-product", /[^\n\s;\'\"\`]{2,}/, "search");
    let sku_field = new FieldData("sku", /[^\n\s;\'\"\`]{2,}/, "search");

    let new_product_data;

    onMount(() => {
        document.addEventListener(tracked_products_events.TRACKED_PRODUCTS_CHANGED, clearPorductDat);
    });

    onDestroy(() => {
        document.removeEventListener(tracked_products_events.TRACKED_PRODUCTS_CHANGED, clearPorductDat);
    });

    const clearPorductDat = () => {
        search_field.clear();
        sku_field.clear();

        new_product_data = undefined;
    }

    const searchProduct = () => {
        if (!verifyFormFields([search_field])) {
            alert("Invalid url");
            return;
        }
        let meli_url = search_field.getFieldValue();
        let meli_id = getMeliIdFromUrl(meli_url).replace("-", "");

        if (meli_id === null) {
            newNotification("No fue posible obtener el id del producto desde la url, el id tiene el formato MLM-XXXXXXX o MLMXXXXXXX");
            return;
        }

        const get_item_request = new GetMeliItemData(bonhart_storage.Token, meli_id, meli_url);

        const on_success = item_data => {
            new_product_data = item_data;
        }

        const on_error = error => {
            console.log(error);
        }

        get_item_request.do(on_success, on_error);
    }

    const trackProduct = () => {
        const track_product_request = new PostTrackedProduct(bonhart_storage.Token, new_product_data, "");
        const sku = sku_field.getFieldValue();

        if (sku === null || sku === "") {
            newNotification("El campo SKU no puede estar vacío");
            return;
        }

        track_product_request.sku = sku;

        const on_success = () => {
            newNotification("Producto agregado a la lista de seguimiento");
            emitTrackProductsChanged(new_product_data);
        }

        const on_error = error => {
            console.log(error);
        }

        track_product_request.do(on_success, on_error);
    }
</script>

<div id="track-product-component">
    <div id="tpc-get-component-form">
        <div id="tpc-gcf-search-wrapper">
            <Input 
                field_data={search_field}
                onEnterPressed={searchProduct}
                input_label="Agregar por url:"
                font_size="var(--font-size-1)"
                input_background="var(--clear-color)"
                input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
            />
        </div>
        <div id="tpc-gcf-sku-wrapper">
            <Input 
                field_data={sku_field}
                input_label="SKU:"
                font_size="var(--font-size-1)"
                input_background="var(--clear-color)"
                input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
            />
        </div>
        <div id="tpc-gcf-controls">
            <button on:click={searchProduct}  id="search-product-btn" class="full-btn">
                <span class="material-symbols-outlined">search</span>
            </button>
            {#if new_product_data !== undefined}
                <button on:click={trackProduct} id="track-product-btn" class="full-btn">
                    <span class="material-symbols-outlined">add</span>
                </button>
            {/if}
        </div>
    </div>
    {#if new_product_data !== undefined}
        <div id="product-preview-wrapper">
            <ProductPreview item_data={new_product_data}/>
        </div>
    {/if}
</div>

<style>
    #track-product-component {
        width: 100%;
        padding: var(--spacing-3) var(--spacing-4);
        border-bottom: 1px solid var(--primary-color-midlight);
    }

    #tpc-get-component-form {
        display: flex;
        align-items: center;
        gap: var(--spacing-4);
    }

    #tpc-gcf-controls {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
    }

    #tpc-gcf-search-wrapper {
        width: 70%;
    }

    #product-preview-wrapper {
        padding: var(--spacing-3) 0 0 0;
    }
</style>