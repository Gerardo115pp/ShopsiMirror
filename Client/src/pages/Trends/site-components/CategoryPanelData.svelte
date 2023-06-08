<script>
    import { emitTrendKeywordSelected }  from '../events';

    export let category_data = {};
    export let selected_product = {};

    const stock_number_formatter = new Intl.NumberFormat('es-MX', {
        style: 'decimal',
        maximumFractionDigits: 0,
        minimumFractionDigits: 0
    });
    const price_number_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        maximumFractionDigits: 3,
        minimumFractionDigits: 2
    });

    const addClickAnimation = e => {
        const target = e.target;
        target.classList.add('blink-1');
        setTimeout(() => {
            target.classList.remove('blink-1');
        }, 500);
    }

    const handleTrendClicked = e => {
        addClickAnimation(e);
        emitTrendKeywordSelected(e.target.innerText);
    }
</script>

<div id="ptp-category-data-wrapper">
    <div id="ptp-cdw-attributes-wrapper">
        <h3 id="ptp-cdw-aw-title" >
            Categoria del producto <span class="highlighted-text">{selected_product.product.name}</span>
        </h3>
        <h4 id="ptp-cdw-aw-category-path">
            {#each category_data.category.path_from_root as category_redux, h}
                {category_redux.name}
                {#if h < category_data.category.path_from_root.length - 1}
                    <span class="highlighted-text material-symbols-outlined">arrow_forward_ios</span>
                {/if}
            {/each}
        </h4>
        <div class="ptp-cdw-aw-attribute">
            <span class="ptp-cdw-aw-attribute-name">Nombre</span>
            <span class="ptp-cdw-aw-attribute-value highlighted-text">
                {category_data.category.name}
            </span>
        </div>
        <div class="ptp-cdw-aw-attribute">
            <span class="ptp-cdw-aw-attribute-name">tu precio</span>
            <span class="ptp-cdw-aw-attribute-value highlighted-text">
                {price_number_formatter.format(selected_product.product.initial_price)}
            </span>
        </div>
        <div class="ptp-cdw-aw-attribute">
            <span class="ptp-cdw-aw-attribute-name">Productos en la categoria</span>
            <span class="ptp-cdw-aw-attribute-value highlighted-text">
                {stock_number_formatter.format(category_data.category.total_items_in_this_category)}
            </span>
        </div>
        <div class="ptp-cdw-aw-attribute">
            <span class="ptp-cdw-aw-attribute-name">Tendencias</span>
            <span class="ptp-cdw-aw-attribute-value highlighted-text">
                {category_data.trends.length}
            </span>
        </div>
    </div>
    <div id="ptp-cdw-trends">
        <h3 id="ptp-cdw-trends-title">
            Palabras tendencia
        </h3>
        <div id="ptp-cdw-trends-container">
            {#if category_data.trends.length > 0}
                {#each category_data.trends as trend}
                    <div on:click={handleTrendClicked} class="trend-wrapper">{trend.keyword}</div>
                {/each}
            {/if}
        </div>
    </div>
</div>

<style>
    #ptp-category-data-wrapper {
        display: flex;
        width: 100%;
        padding: var(--spacing-2) var(--spacing-2);
    }

    /* #ptp-category-data-wrapper * {
        border: 1px solid red;
    } */

    /* Attributes */

    #ptp-cdw-attributes-wrapper {
        width: 70%;
    }

    #ptp-cdw-attributes-wrapper > * {
        margin-top: var(--spacing-2);
    }    

    #ptp-cdw-aw-title {
        font-size: var(--font-size-1);
        text-transform: uppercase;
        display: flex;
        align-items: center;
    }

    #ptp-cdw-aw-title > .highlighted-text {
        text-transform: none;
    }

    #ptp-cdw-aw-title > .highlighted-text::before {
        content: ": ";
        color: var(--dark-light-color);
    }

    #ptp-cdw-aw-category-path {
        display: flex;
        align-items: center;
        font-size: var(--font-size-small);
        color: var(--dark-light-color);
    }

    #ptp-cdw-aw-category-path > .highlighted-text {
        font-size: var(--font-size-small);
    }

    .ptp-cdw-aw-attribute-name {
        color: var(--dark-light-color);
        text-transform: uppercase;
    }

    .ptp-cdw-aw-attribute-name::after {
        content: ": ";
    }

    /* Trends */

    #ptp-cdw-trends {
        width: 30%;
    }

    #ptp-cdw-trends-title {
        font-size: var(--font-size-2);
        color: var(--primary-color-midlight);
        padding: var(--spacing-1) var(--spacing-1);
        text-transform: uppercase;
    }

    #ptp-cdw-trends-container {
        height: min(30ch, 30vh);
        background: var(--primary-color-light);
        overflow-y: auto;
        color: white;
        box-shadow: var(--inset-shadow-2);
    }

    .trend-wrapper {
        cursor: default;
        background-color: var(--tertiary-color-midlight);
        padding: var(--spacing-2) var(--spacing-1);
        transition: all .6s ease-in;
        border-bottom: 1px solid white;
    }

    /* .trend-wrapper:hover {
    } */
    
    .trend-wrapper:last-child {
        border-bottom: none;
    }


</style>