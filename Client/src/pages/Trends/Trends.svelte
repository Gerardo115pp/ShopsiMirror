<script>
    import { GetCategoryTrendsRequest, ProductsSearchRequest, PostCompetitorProductRequest } from "../../libs/HttpRequests";
    import bonhart_storage, { standard_generic_stores } from "../../libs/bonhart-storage";
    import CategoryPanelData from "./site-components/CategoryPanelData.svelte";
    import TrendItemsContainer from "./site-components/TrendItemsContainer.svelte";
    import { trends_events } from "./events";
    import { newNotification } from "../../components/notifications/events";
    import { onMount, onDestroy } from "svelte";
    
    export let params = {};

    const { meli_id } = params;
    const selected_product = bonhart_storage.readGeneric(standard_generic_stores.PRODUCTS, 'selected_product');
    console.log(selected_product);

    let competitors = new Set();
    let category_data = undefined;
    let selected_trend = undefined; // this will be the query to search for products, its the keyword of the trend
    let trend_items = []; // this will be the list of products that match the selected trend
    $:if (selected_product.competitors !== undefined) {
        competitors = new Set(selected_product.competitors.map(c => c.meli_id));
        console.log(competitors);
    }


    onMount(() => {
        document.addEventListener(trends_events.TREND_KEYWORD_SELECTED,getTrendProducts);

        document.addEventListener(trends_events.TREND_ITEM_COMPETES, addCompetitorProduct);

        getCategoryTends();
    });

    onDestroy(() => {
        document.removeEventListener(trends_events.TREND_KEYWORD_SELECTED,getTrendProducts);

        document.removeEventListener(trends_events.TREND_ITEM_COMPETES, addCompetitorProduct);
    });

    const getCategoryTends = () => {
        const get_category_trends_request = new GetCategoryTrendsRequest(bonhart_storage.Token, selected_product.product.category_id);

        const on_success = data => {
            category_data = data;
        }

        const on_error = error_code => {
            switch (error_code) {
                case 401:
                    newNotification("Aparentemente no tienes una cuenta de mercadolibre vinculada a tu cuenta del sistema, por favor vincula una cuenta de mercadolibre para poder usar esta funcionalidad");
                    break;
                case 403:
                    newNotification("Parece que alguien esta haciendo algo raro, este incidente sera reportado");
                    break;
                default:
                    newNotification(`Ocurrio un error desconocido, reporta el siguiente codigo: ${error_code}`);
                    break;
            }
        }

        get_category_trends_request.do(on_success, on_error);
    }

    const getTrendProducts = e => {
        const trend_keyword = e.detail;
        const search_request = new ProductsSearchRequest(bonhart_storage.Token);
        search_request.search_query = trend_keyword;

        const on_success = response => {
            trend_items = response.results;
            console.log('trend_products', trend_items);
        }

        const on_error = status_code => {
            console.log('error', status_code);
            newNotification("Error al obtener los productos de la tendencia");
        }

        search_request.do(on_success, on_error);
    }

    const addCompetitorProduct = e => {
        const { detail:item_data } = e;
        const add_competitor_product_request = new PostCompetitorProductRequest(bonhart_storage.Token);
        add_competitor_product_request.competes_with = selected_product.product.sku;
        add_competitor_product_request.item_data = item_data;

        const on_success = response => {
            newNotification(`Producto agregado a la lista de competidores de ${selected_product.product.sku}`);
        }

        const on_error = status_code => {
            newNotification("Error al agregar el producto a la lista de competidores");
        }

        add_competitor_product_request.do(on_success, on_error);
    }




</script>

<main id="product-trends-page">
    <div id="ptp-category-panel">
        {#if category_data !== undefined}
             <CategoryPanelData {category_data} {selected_product}/>
        {/if}
    </div>
    <div id="ptp-trend-products-container">
        <TrendItemsContainer our_product_meli_id={meli_id} {competitors}  items={trend_items}/>
    </div>
</main>

<style>
    #product-trends-page {
        margin-top: var(--navbar-height);
    }
</style>