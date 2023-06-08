<script>
    import { GetProductCustomQueriesRequest, ProductsSearchRequest, DeleteCustomQueryRequest, PostCompetitorProductRequest } from "../../../libs/HttpRequests";
    import { newNotification } from "../../../components/notifications/events";
    import PositionSearchItem from "./PositionSearchItem.svelte";
    import bonhart_storage, { standard_generic_stores } from "../../../libs/bonhart-storage";
    import { product_positioning_events } from "../events";
    import { onMount, onDestroy } from "svelte";

    export let current_sku = undefined;
    export let our_product_meli_id = undefined;
    export let competitors = new Set();

    let product_custom_queries = [];
    let custom_query_search_products = [];
    let current_custom_query = {}; // {meli_id: "", keyword: "", sku: ""}
    current_custom_query.our_product_position = "?";
    $: requestProductCustomQueries(), current_sku;
    $: setSavedPosition(product_custom_queries);

    onMount(() => { 
        document.addEventListener(product_positioning_events.CUSTOME_QUERYS_CHANGED, requestProductCustomQueries);
        document.addEventListener(product_positioning_events.PRODUCT_COMPETES, createNewCompetitorProducts);
    });

    onDestroy(() => {
        document.removeEventListener(product_positioning_events.CUSTOME_QUERYS_CHANGED, requestProductCustomQueries);
        document.removeEventListener(product_positioning_events.PRODUCT_COMPETES, createNewCompetitorProducts);
    });

    function requestProductCustomQueries() {
        if (current_sku === undefined) {
            return;
        }

        const get_product_custom_queries_request = new GetProductCustomQueriesRequest(bonhart_storage.Token);
        get_product_custom_queries_request.sku = current_sku;

        const on_success = (response) => {
            let product_number = 0;
            for (let custom_query of response) {
                custom_query.our_product_position = "?";
                custom_query.id = product_number;
                product_number++;
            }
            response = setSavedPosition(response);
            product_custom_queries = response;
        };

        const on_error = (error) => {
            newNotification(`Error al obtener los terminos de busqueda: ${error}`);
        };

        get_product_custom_queries_request.do(on_success, on_error);
    }

    function createNewCompetitorProducts(product_data) {
        
        const { detail:item_data } = product_data;

        const request = new PostCompetitorProductRequest(bonhart_storage.Token);
        request.competes_with = current_sku;
        request.item_data = item_data;

        if (current_sku === undefined) {
            console.log("Current sku is undefined when trying to create a new competitor product from the product positioning page");
            return;
        }

        const on_success = (response) => {
            newNotification("Producto agregado a la lista de competidores");
            // competitors.add(item_data.id);
            competitors = new Set([...competitors, item_data.id]);
        };
        
        const on_error = (error_code) => {
            newNotification(`Error al agregar el producto a la lista de competidores: ${error_code}`);
        };
        
        request.do(on_success, on_error);
        
    }
    
    const getOurProductPosition = products_list => {
        for (let h = 0; h < products_list.length; h++) {
            if (products_list[h].id === our_product_meli_id) {
                return `${h + 1}`;
            }
        }

        return "50+";
    };

    const getCustomTrendProducts = custom_query => {
        if (custom_query.id === current_custom_query.id) {
            current_custom_query = {};
            return;
        }
        const search_request = new ProductsSearchRequest(bonhart_storage.Token);
        search_request.search_query = custom_query.keyword;
        search_request.limit = 50;
        
        // Set the active product class to the current product and remove the previous products list
        custom_query_search_products = [];
        console.log(custom_query);
        current_custom_query = custom_query;
        current_custom_query.our_product_position = "50+";

        const on_success = response => {
            custom_query_search_products = response.results;
            current_custom_query.our_product_position = getOurProductPosition(custom_query_search_products);
            bonhart_storage.writeGeneric(standard_generic_stores.POSITIONING, current_sku, product_custom_queries);
            product_custom_queries = [...product_custom_queries];
        };

        const on_error = error => {
            newNotification(`Error al obtener los productos: ${error}`);
        };

        search_request.do(on_success, on_error);
    }

    const deleteProductCustomQuery = custom_query => {
        const delete_custom_query_request = new DeleteCustomQueryRequest(bonhart_storage.Token);
        delete_custom_query_request.sku = current_sku;
        delete_custom_query_request.keyword = custom_query.keyword;

        const on_success = response => {
            requestProductCustomQueries();
        };

        const on_error = error => {
            newNotification(`Error al eliminar el termino de busqueda: ${error}`);
        };

        delete_custom_query_request.do(on_success, on_error);
    }

    function setSavedPosition(new_custom_queries) {
        const existing_keywords = new Set(new_custom_queries.map(custom_query => custom_query.keyword));
        let cached_custom_queries = bonhart_storage.readGeneric(standard_generic_stores.POSITIONING, current_sku);
        if (cached_custom_queries === null) {
            cached_custom_queries = [];
        }

        cached_custom_queries = cached_custom_queries.filter(cached_custom_query => existing_keywords.has(cached_custom_query.keyword));
        const keywords_lookup = new Set(cached_custom_queries.map(custom_query => custom_query.keyword));

        for (let custom_query of new_custom_queries) {
            if (!keywords_lookup.has(custom_query.keyword)) {
                cached_custom_queries.push(custom_query);
            }
        }

        return cached_custom_queries;
    }

</script>

<div id="saved-querys">
    {#if current_sku !== undefined}
         <h3 id="sq-title">
            Terminos guardados para <span class="highlighted-text">{current_sku}</span>
         </h3>
         <div id="sq-container">
            {#each product_custom_queries as query}
                <div id="sq-{query.meli_id}-item" class="sq-item">
                    <span class="sq-item-attribute sq-item-text highlighted-text">{query.keyword}</span>
                    <span class="sq-item-attribute sq-item-position">tu posicion: <span class="highlighted-text">{query.our_product_position}</span></span>
                    <div class="sq-item-attribute sq-item-actions">
                        <span on:click={() => getCustomTrendProducts(query)} class="material-symbols-outlined full-btn">search</span>
                        <span on:click={() => deleteProductCustomQuery(query)} class="material-symbols-outlined danger-btn">delete</span>
                    </div>
                </div>
                {#if current_custom_query.id === query.id}
                    <div id="sq-{query.meli_id}-products" class="sq-products">
                        {#each custom_query_search_products as product, position}
                            <PositionSearchItem is_competitor={competitors.has(product.id)} is_ours={product.id === our_product_meli_id} position={position+1} item_data={product} />
                        {/each}
                    </div>
                {/if}
            {/each}
         </div>
    {/if}
</div>

<style>
    #sq-title {
        color: var(--dark-light-color);
    }

    #sq-container {
        padding: var(--spacing-3) 0 0 0;
    }

    .sq-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--spacing-2) var(--spacing-4);
        border-bottom: 1px solid var(--dark-light-color);
    }

    .sq-item:last-child {
        border-bottom: none;
    }

    .sq-item-attribute {
        min-width: var(--spacing-h3);
    }
</style>