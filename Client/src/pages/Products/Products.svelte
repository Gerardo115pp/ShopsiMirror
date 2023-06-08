<script>
    import { GetOurProductsRequest, GetLatestPerformanceRecords } from '../../libs/HttpRequests';
    import { newNotification } from '../../components/notifications/events';
    import TimeRangeFilter from './page-components/TimeRangeFilter.svelte';
    import { isLoggedIn, logout } from '../../libs/dandelion-utils';
    import CTloader from '../../components/Loaders/CTloader.svelte';
    import OurProduct from './page-components/OurProducts.svelte';
    import bonhart_storage from '../../libs/bonhart-storage';
    import { onMount } from 'svelte';
    
    

    let products = []; // {category_id:str, competes_with:str, name:str, price:float, meli_url:str, competitors:[]Product, condition: str, domain_id:str, initial_price:float, meli_id: str, product_id: str, secure_thumbnail:str, seller_id:int, site_id: str, sku:str, status:str}
    let performance_records = {};
    let is_performance_records_loading = false;
    
    let performance_recorded_between = {} // {first: str, last: str}

    isLoggedIn() // check if user is logged in, if its not then it will redirect to login page

    onMount(() => {
        // getPerformanceRecords(); // on success calls getOurProducts()
        getOurProducts();
    });
    


    const getOurProducts = () => {
        const new_products_requests = new GetOurProductsRequest(bonhart_storage.Token);
        
        const on_success = data => {
            products = Object.values(data);
            is_performance_records_loading = true;
            getPerformanceRecords();
        };

        const on_error = error_code => {
            if (error_code === 401) {
                newNotification('Por favor inicia sesión de nuevo');
                logout();
            }

            newNotification(`Hubo un error al obtener los productos, reporta el siguiente codigo: ${error_code}`);
        };
        
        new_products_requests.do(on_success, on_error);
        
    }

    const getPerformanceRecords = () => {
        const new_performance_records_request = new GetLatestPerformanceRecords(bonhart_storage.Token); // this request is the one that takes the most time
        const on_success = data => {
            performance_records = data.records; 
            // e.g data.recorded_between = {first: "Mon, 18 Jul 2022 14:57:57 GMT", last: "Mon, 18 Jul 2022 14:57:57 GMT"}
            performance_recorded_between = {
                first: new Date(data.recorded_between.first),
                last: new Date(data.recorded_between.last)
            };
            is_performance_records_loading = false;
        };

        const on_error = error_code => {
            if (error_code === 401) {
                newNotification('Por favor inicia sesión de nuevo');
                logout();
            }

            newNotification(`Hubo un error al obtener los productos, reporta el siguiente codigo: ${error_code}`);
            is_performance_records_loading = false;
        };

        new_performance_records_request.do(on_success, on_error);
    }
</script>

<main id="meli-tracked-products">
    <div id="mtp-top-stats-container">
        <div id="mts-stat-our-products-count" class="mts-stats"><span>Nuestros productos</span>{products.length}</div>
        <div id="mts-stat-competitors-count" class="mts-stats"><span>Competidores</span>410</div>
    </div>
    <div id="mtp-top-filters">
        {#if Object.keys(performance_records).length > 0}
             <TimeRangeFilter {performance_recorded_between} />
        {/if}
    </div>
    {#if products.length > 0}
        <!-- if there are no products loaded, show the loading animation. if there are but performance records are still loading then show the animation and the products list without pr data. when they both have loaded, remove loading animation -->
        {#if is_performance_records_loading}
            <div id="products-loader-container" class="small-loader">
                <CTloader />
            </div>
        {/if}
         <div id="mtp-products-container">
             {#each products as product}
                 <OurProduct performance_recorded_between={performance_recorded_between}  product_data={product} performance_records={performance_records[product.product.product_id] ?? []}/>
             {/each}
         </div>
    {:else}
         <div id="products-loader-container" class="large-loader">
                <CTloader />
         </div>
    {/if}
</main>

<style>
    #mtp-top-stats-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: var(--spacing-3);
        margin-top: var(--navbar-height);
        border-bottom: 1px solid var(--primary-color);
        border-top: 1px solid var(--primary-color);
        background: var(--primary-gradient);
        box-shadow: 0px 0px 15px 6px rgba(0, 0, 0, 0.1);
    }

    .mts-stats {
        color: var(--secondary-color-dark);
    }
    
    .mts-stats span {
        color: var(--clear-color);
    }

    .mts-stats span::after {
        content: ':';
        margin: 0 var(--spacing-1) 0 0;
    }

    #mtp-products-container {
        --products-container-width: 100vw;

        overflow-y: auto;
        overflow-x: hidden;
        width: var(--products-container-width);
        height: calc(var(--spacing-h1) * 1.2);
        border: 1px solid var(--primary-color);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: var(--spacing-3) 0;
    }

    #mtp-top-filters {
        padding: var(--spacing-3);
    }

    #products-loader-container {
        display: grid;
        place-items: center;
        width: 100%;
    }
    
    .large-loader {
        padding: var(--spacing-h3) 0;
    }

    .small-loader {
        padding: var(--spacing-3) 0;
    }

</style>