<script>
    
    import { ProductsSearchRequest, PostCompetitorProductRequest, GetProductCompetitorsRequest, PostOwnerProductRequest, GetTrackedProducts, PostTrackedProduct } from "../../libs/HttpRequests";
    import { newNotification } from "../../components/notifications/events";
    import SearchFilters from './site-components/SearchFilters.svelte';
    import { isLoggedIn, PriceRange } from "../../libs/dandelion-utils";
    import viewport from "../../components/viewport_actions/useViewportActions";
    import PriceFilter from './site-components/PriceFilter.svelte';
    import PricePlot from "./site-components/PricePlot.svelte";
    import bonhart_storage from "../../libs/bonhart-storage";
    import MeliItem from "./site-components/MeliItem.svelte";
    import SkuInput from './site-components/SKUinput.svelte';
    import { emitSkuChanged } from "./events";
    import Input from "../../components/Input/Input.svelte";
    import FieldData from "../../libs/FieldData";
    
    let create_product_mode = false; // this will be true if the user entered a sku that is not being used by one of OUR products, but it could be used by a competitor or a tracked product

    let last_used_query = undefined;
    let search_results = [];
    let search_filters = [];
    let filtered_results = [];
    let owner_id = undefined;
    let total_results = Infinity; // this is the total number of results for the last_used_query, we get this information after making the first search request
    let price_range = new PriceRange(0, Infinity);
    let current_sku = "";
    let current_product_id = ""; 
    let competitors = new Set();
    let tracked_products = new Set();

    tracked_products = getTrackingProducts();

    $: filtered_results = filterSearchItems(search_results, price_range), search_filters;
    $: getCompetitors(current_product_id);

    let my_item_price =-1;
    isLoggedIn(); // if user is not logged in, it will redirect to login page

    // FIELDS

    let search_field = new FieldData("search-field", /[\p{L}\p{N}\s0-9]{3,20}/, "Buscar");
    let price_field = new FieldData("price-field", /\d+(\.\d+)?/, "Precio");


    const getCompetitors = product_id => {
        if (!product_id) {
            competitors = new Set();
            return;
        }

        const get_product_competitors_request = new GetProductCompetitorsRequest(bonhart_storage.Token);
        get_product_competitors_request.product_id = product_id;

        const on_success = (response) => {
            console.log(response);
            let meli_ids = response.map(item => item.meli_id);
            console.log(meli_ids);
            competitors = new Set(meli_ids);
        };

        const on_error = (error) => {
            newNotification(`Error al obtener los competidores: ${error}`);
            competitors = new Set();
        };

        get_product_competitors_request.do(on_success, on_error);
    };

    function getTrackingProducts() {
        const get_tracked_products_request = new GetTrackedProducts(bonhart_storage.Token);
        const on_success = (response) => {
            console.log(response);
            let meli_ids = response.map(item => item.meli_id);
            console.log(meli_ids);
            tracked_products = new Set(meli_ids);
        };

        const on_error = (error) => {
            newNotification(`Error al obtener los productos seguidos: ${error}`);
            tracked_products = new Set();
        };

        get_tracked_products_request.do(on_success, on_error);
    };

    const search = () => {
        console.log("searching");

        const current_search_query = search_field.getFieldValue();
        if (total_results <= search_results.length && last_used_query === current_search_query) {
            console.log("no more results");
            return;
        }

        // the search offset is handled by the server. the client is only responsible to stop sending requests when the search_results length >= total_results
        const request = new ProductsSearchRequest(bonhart_storage.Token);
        request.search_query = current_search_query;

        const on_success = response => {
            search_results = response.results;
            total_results = response.total <= 1000 ? response.total : 1000; // we limit the total results to 1000 because meli api imposes this limit
            owner_id = response.owner_id;

            // check if the filtered_results > greater then 20, else, search again
            if (search_results.length <= total_results) {
                const filtered_results = filterSearchItems(search_results, price_range);
                if (filtered_results.length < 20) {
                    search();
                }
            }

            console.log(`total results: ${total_results}\n search results: ${search_results.length}`);
            last_used_query = search_field.getFieldValue();
        };

        const on_error = status_code => {
            switch (status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                case 401:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 401");
                    break;
                case 404:
                    newNotification("No se encontraron resultados");
                    break;
                default:
                    create_product_mode = true;
                    newNotification(`Se encontro un error inesperado al buscar tiems, favor de reportarlo: ${status_code}`);
            }
        };
        
        request.do(on_success, on_error);
    }

    const filterItemsOutPriceRange = (items, price_range) => {
        return items.filter(item => {
            return price_range.inRange(item.price);
        });
    }

    function filterSearchItems(search_items, price_range) {
        search_items = filterItemsOutPriceRange(search_items, price_range);
        if (search_filters.length == 0) {
            // if there are no filters, return all items
            return search_items;
        }
        let filtered_items  = [];

        search_items.forEach((item, h) => {
            // the KeywordFilter class automatically checks the text as lowercase
            let item_name = item.name;
            let item_attributes = item.attributes;
            
            // check if all the filters are in the item name or attributes
            let matches_filter = search_filters.every((filter) => {
                let matches_attribute = filter.match(item_attributes);
                let matches_name = filter.match(item_name);
                console.log(`filter: ${filter}\nmatches_attribute: ${matches_attribute}\nmatches_name: ${matches_name}`);
                return (matches_name || matches_attribute);
            });

            console.log(`item '${item_name}', '${item_attributes}' matches filter: ${matches_filter}`);
            // add the item to the filtered items, if it matches all the filters
            if (matches_filter) {
                filtered_items.push(item);
            }
        });

        return filtered_items;
    }

    const setPrice = e => {
        if(e.key === "Enter"){
            e.target.value = e.target.value.replace(/[^\d]/g, "");
            e.target.blur();
            my_item_price = parseFloat(e.target.value);
        }
    }

    const addCompetitorProduct = item_data => {
        if (current_sku === "") {
            newNotification("No se ha ingresado un SKU valido");
            return;
        }

        const create_product_request = new PostCompetitorProductRequest(bonhart_storage.Token);
        create_product_request.item_data = item_data;
        create_product_request.competes_with = current_sku;

        const on_success = () => {
            newNotification("Producto agregado exitosamente");
        };
        
        const on_error = status_code => {
            switch (status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                case 401:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 401");
                    break;
                case 404:
                    newNotification("No se encontraron resultados");
                    break;
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
            }
        };

        create_product_request.do(on_success, on_error);
    }
    
    const addOwnerProduct = item_data => {
        if (!create_product_mode) {
            console.log("not in create product mode, but trying to add owner product");
            return;
        }

        const create_product_request = new PostOwnerProductRequest(bonhart_storage.Token);
        create_product_request.item_data = item_data;
        create_product_request.sku = current_sku;

        const on_success = () => {
            emitSkuChanged(current_sku);
            newNotification("Producto trackeado exitosamente");
        };
        
        const on_error = status_code => {
            switch (status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                case 401:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 401");
                    break;
                case 404:
                    newNotification("No se encontraron resultados");
                    break;
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
            }
        };

        create_product_request.do(on_success, on_error);
    }

    const addTrackedProduct = item_data => {
        if (current_sku === "") {
            newNotification("No se ha ingresado un SKU valido");
            return;
        }

        const create_product_request = new PostTrackedProduct(bonhart_storage.Token, item_data, current_sku);

        const on_success = () => {
            emitSkuChanged(current_sku);
            newNotification("Producto trackeado exitosamente");
        };
        
        const on_error = status_code => {
            switch (status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                case 401:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 401");
                    break;
                case 404:
                    newNotification("No se encontraron resultados");
                    break;
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
            }
        };

        create_product_request.do(on_success, on_error);
    } 


    let sorted_products = [];
    
    $: sorted_products = [...filtered_results].sort((a, b) => {
        return a.price - b.price;
    });




</script>


<main id="home-page-content">
    <div id="hpc-control-panel">
        <div id="hpc-search-panel">
            <div class="hcp-control-input" id="hpc-sp-search-bar-container">
                <Input 
                    field_data={search_field}
                    onEnterPressed={search}
                    input_label="Buscar"
                    font_size="var(--font-size-1)"
                    input_background="var(--clear-color)"
                    input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
                />
            </div>
            <div class="hcp-control-input" id="hpc-sp-my-price-container">
                <Input 
                    field_data={price_field}
                    onEnterPressed={setPrice}
                    input_label="Mi Precio"
                    font_size="var(--font-size-small)"
                    input_background="var(--clear-color)"
                    input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
                />
            </div>
            <div class="hcp-control-input" id="hpc-sp-my-product-sku">
                <SkuInput bind:create_product_mode={create_product_mode} bind:current_sku={current_sku} bind:current_product_id={current_product_id}/>
            </div>
            <div class="hcp-control-input" id="hpc-sp-price-range">
                <PriceFilter bind:price_range={price_range}/>
            </div>
            <div class="hcp-control-input" id="hpc-sp-search-filters-wrapper">
                <SearchFilters bind:filters={search_filters} />
            </div>
        </div>
        <PricePlot {my_item_price} search_results={sorted_products}/>
    </div>
    <div id="hpc-results">
        {#if filtered_results.length > 0}
            <div id="hpc-loaded-results">
                {#each filtered_results as result, h}
                    <div class="hpc-meli-item-wrapper">
                        <MeliItem
                            is_ours={result.seller_id === owner_id} 
                            is_competitor={competitors.has(result.id)}
                            is_tracked={tracked_products.has(result.id)}
                            {create_product_mode}
                            my_price={my_item_price} 
                            item_data={result} 
                            add_competitor_callback={addCompetitorProduct}
                            add_our_product_callback={addOwnerProduct}
                            add_tracked_item_callback={addTrackedProduct}
                        />
                    </div>
                {/each}
                <div use:viewport on:viewportEnter={search} class="hpc-items-end">
                    <div class="hpc-items-end-text">
                        <p>Fin de la lista</p>
                    </div>
                </div>
            </div>
        {:else}
            <div id="hpc-no-results">
                <h3>Nothing to see here</h3>
            </div>
        {/if}
    </div>
</main>


<style>

    
    /*=============================================
    =            Search Bar            =
    =============================================*/

    #hpc-control-panel {
        display: flex;
        padding: var(--spacing-3);
        background: var(--primary-gradient);
        box-shadow: var(--inset-shadow-2);
        margin-top: var(--navbar-height);
    }

    #hpc-search-panel {
        width: 50%;
        display: grid;
        grid-template: repeat(4, 1fr) / repeat(6, 1fr);
        grid-gap: var(--spacing-2);
        grid-template-areas:
            'sb sb sb sb sb sb'
            'sf sf sf sf sf sf'
            'sf sf sf sf sf sf'
            'pp pp pf pf sk sk';
            ;
        /* sb= search bar, pp=product price, sf= search filters, pf=price filter, sk=sku field */
        padding: 0 3vw 0 0;
    }
    
    #hpc-sp-search-bar-container {
        grid-area: sb;
    }

    #hpc-sp-my-price-container {
        grid-area: pp;
    }

    #hpc-sp-search-filters-wrapper {
        grid-area: sf;
    }

    #hpc-sp-my-product-sku {
        grid-area: sk;
    }

    #hpc-sp-price-range {
        grid-area: pf;
    }


    #hpc-search-panel .hcp-control-input {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }



    
    /*=============================================
    =            Results            =
    =============================================*/
    
    #hpc-no-results {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 90vh;
    }

    #hpc-no-results h3 {
        font-size: 2rem;
        font-style: italic;
        color: var(--secondary-color-light);
    }

    #hpc-loaded-results {
        height: 60vh;
        overflow-y: scroll;
    }
    
    #hpc-loaded-results::-webkit-scrollbar {
        display: none;
    }

    .hpc-items-end {
        display:grid;
        background: var(--primary-gradient);
        padding: var(--spacing-2);
        color: white;
        place-items: center;
    }

</style>