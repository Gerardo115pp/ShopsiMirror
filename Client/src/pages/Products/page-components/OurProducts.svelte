<script>
    import bonhart_storage, { standard_generic_stores } from "../../../libs/bonhart-storage";
    import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
    import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
    import { products_events } from '../events';
    import { push } from 'svelte-spa-router';
    import { onMount, onDestroy } from 'svelte';
    import dayjs from 'dayjs';

    dayjs.extend(isSameOrBefore);
    dayjs.extend(isSameOrAfter);

    window.dayjs = dayjs;

    export let performance_records;
    export let performance_recorded_between;

    let filter_start_date = performance_recorded_between.first;
    let filter_end_date = performance_recorded_between.last;

    export let product_data = {
        product: {
            "category_id": "",
            "competes_with": "",
            "condition": "",
            "domain_id": "",
            "initial_price": 0.0,
            "meli_id": "",
            "meli_url": "",
            "name": "No product set",
            "product_id": "",
            "secure_thumbnail": "",
            "seller_id": 0,
            "site_id": "",
            "sku": "",
            "status": ""
        },
        competitors: []
    };

    const empty_performance_record = {
                "current_price": "?",
                "visits": "?",
                "sales": "?",
                "stock": "?"
            };
    let performance_record;
    $: performance_record = getPerformanceRecord(), filter_start_date, filter_end_date;


    onMount(() => {
        document.addEventListener(products_events.TIME_RANGE_CHANGED, handleTimeRangeChange);
    });

    onDestroy(() => {
        document.removeEventListener(products_events.TIME_RANGE_CHANGED, handleTimeRangeChange);
    });



    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    });

    const handleTimeRangeChange = e => {
        const { first:start_date, last:end_date } = e.detail;
        filter_start_date = start_date || performance_recorded_between.first;
        filter_end_date = end_date || performance_recorded_between.last;
    }

    function getPerformanceRecord() {

        if (performance_records.length === 0) {
            return empty_performance_record;
        }
        let pr_data = performance_records[0];

        if(!dayjs(filter_start_date).isSame(dayjs(performance_recorded_between.first), 'day') || !dayjs(filter_end_date).isSame(dayjs(performance_recorded_between.last), 'day')) {

            let start_pr = performance_records.reverse().find(pr => dayjs(pr.recorded_date).isSameOrAfter(filter_start_date, 'day'));

            // DEBUG
                // let start_pr = performance_records[0];

                // for(let pr of performance_records.reverse()) {
                //     console.log(`checking if ${dayjs(pr.recorded_date).format('YYYY-MMM-DD')} is after or same ${dayjs(filter_start_date).format('YYYY-MMM-DD')}: ${dayjs(pr.recorded_date).isSameOrAfter(filter_start_date, 'day')}`);
                //     if(dayjs(pr.recorded_date).isSameOrAfter(filter_start_date, 'day')) {
                //         console.log(`setting start_pr to ${dayjs(pr.recorded_date).format('YYYY-MMM-DD')}`);
                //         start_pr = pr;
                //         break;
                //     }
                // }
            // debug
            
            let end_pr = performance_records.reverse().find(pr => dayjs(pr.recorded_date).isSameOrBefore(filter_end_date, 'day')); // find the first performance record before or on the end date
            
            //DEBUG
                // console.log(`start: ${dayjs(filter_start_date).format('YYYY-MM-DD')}, end: ${dayjs(filter_end_date).format('YYYY-MM-DD')}`);
                // console.log(`start_pr: `, start_pr.recorded_date);
                // console.log(`end_pr: `, end_pr.recorded_date);
                // for(let pr of performance_records) {
                //     console.log(pr.recorded_date);
                // }
            // debug

            if (!end_pr || !start_pr) {
                return empty_performance_record;
            } 

            pr_data = {
                recorded_date: dayjs(filter_start_date).format('YYYY-MM-DD'),
                current_price: end_pr.price,
                price_change: end_pr.current_price - start_pr.current_price,
                price_change_percentage: ((end_pr.current_price - start_pr.current_price) / start_pr.current_price) * 100,
                sales: end_pr.sales,
                sales_change: end_pr.sales - start_pr.sales,
                sales_change_percentage: ((end_pr.sales - start_pr.sales) / start_pr.sales) * 100,
                visits: end_pr.visits,
                visits_change: end_pr.visits - start_pr.visits,
                visits_change_percentage: ((end_pr.visits - start_pr.visits) / start_pr.visits) * 100,
                stock: end_pr.stock
            };


        }
        return pr_data;
    }

    const goToProductDetails = () => {
        bonhart_storage.writeGeneric(standard_generic_stores.PRODUCTS, 'selected_product', product_data);
        console.log(bonhart_storage.readGeneric(standard_generic_stores.PRODUCTS, 'selected_product'));
        push(`/product-details`);
    }

</script>

<div class="our-product-container">
    <div class="opc-product-attribute opc-product-image">
        <img src={product_data.product.secure_thumbnail} alt={product_data.product.name}/>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">SKU</span>
        <span class="opc-pa-value">{product_data.product.sku}</span>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Estado</span>
        <span class="opc-pa-value">{product_data.product.status}</span>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Nombre</span>
        <span class="opc-pa-value">{product_data.product.name}</span>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Precio</span>
        <span class="opc-pa-value">{!isNaN(performance_record.current_price) ? price_formatter.format(performance_record?.current_price ?? product_data.product.initial_price) : price_formatter.format(product_data.product.initial_price) }</span>
    </div>
    {#if performance_record?.price_change !== undefined}
        <div class="opc-product-attribute">
            <span class="opc-pa-label">D/precio</span>
            <span class="opc-pa-value">{performance_record.price_change ?? "?"}</span>
        </div>
    {/if}
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Competidores</span>
        <span class="opc-pa-value">{product_data.competitors.length}</span>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Ventas</span>
        <span class="opc-pa-value">{performance_record.sales ?? "?"}</span>
    </div>
    {#if performance_record?.sales_change !== undefined}
        <div class="opc-product-attribute">
            <span class="opc-pa-label">D/ventas</span>
            <span class="opc-pa-value">{performance_record.sales_change ?? "?"}</span>
        </div>
    {/if}
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Visitas</span>
        <span class="opc-pa-value">{performance_record.visits ?? "?"}</span>
    </div>
    {#if performance_record?.visits_change !== undefined}
        <div class="opc-product-attribute">
            <span class="opc-pa-label">D/visitas</span>
            <span class="opc-pa-value">{performance_record.visits_change ?? "?"}</span>
        </div>
    {/if}
    <div class="opc-product-attribute">
        <span class="opc-pa-label">Stock</span>
        <span class="opc-pa-value">{performance_record.stock ?? "?"}</span>
    </div>
    <div class="opc-product-attribute">
        <span class="opc-pa-label">ID</span>
        <span class="opc-pa-value">{product_data.product.meli_id}</span>
    </div>
    <div class="opc-product-actions">
        <button on:click={goToProductDetails} class="full-btn">
            <span class="material-symbols-outlined">
                zoom_in_map
            </span>
        </button>
    </div>
</div>

<style>
    .our-product-container {
        --opc-box-width: calc(var(--products-container-width) * 1);

        display: flex;
        width: var(--opc-box-width);
        align-items: center;
        gap: var(--spacing-2);
        padding: var(--spacing-1);
        border: 1px solid var(--primary-color);
    }

    .our-product-container:first-of-type {
        border: none;
    }

    .opc-product-attribute.opc-product-image {
        width: calc(var(--spacing-3)*1.7);
        margin-right: var(--spacing-2);
    }
    /* Debug */
    /* .our-product-container * {
        border : 1px solid red;
    } */

    .opc-product-image img {
        width: 100%;
    }
    
    .opc-product-attribute {
        width: calc(var(--opc-box-width) / 9.5);
        font-size: calc(var(--font-size-small)*0.8);
    }

    .opc-pa-label {
        color: var(--primary-color);
    }

    .opc-pa-label::after {
        content: ":";
    }

    .opc-product-actions {
        display: flex;
        width: calc(var(--opc-box-width) / 7);
        justify-content: center;
        gap: var(--spacing-1);
    }
  

</style>