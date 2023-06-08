<script>
    import { emitTrendItemCompetes } from "../events";


    export let item_data = {}
    export let is_ours = null;
    export let is_competitor = null;
    console.log(`TrendItem: ${item_data.id} is_ours: ${is_ours} is_competitor: ${is_competitor}`)

    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 3
    });

    const handleAddCompetitor = () => {
        emitTrendItemCompetes(item_data);
    }
</script>

<div class="tic-trend-item">
    <div class="ti-image">
        <a href="{item_data.url}">
            <img src="{item_data.thumbnail}" alt="{item_data.name}">
        </a>
    </div>
    <div class="ti-attributes">
        <div class="ti-attribute ti-name">
            <span class="ti-attribute-label">Name</span>
            <span class="ti-attribute-value">
                {#if is_ours}
                    <span class="ti-attribute-value-ours">(tuyo)</span>
                {:else if is_competitor}
                    <span class="ti-attribute-value-competitor">(competidor)</span>
                {/if}    
                {item_data.name}
            </span>
        </div>
        <div class="ti-attribute">
            <span class="ti-attribute-label">Precio</span>
            <span class="ti-attribute-value">{price_formatter.format(item_data.price)}</span>
        </div>
        <div class="ti-attribute">
            <span class="ti-attribute-label">Condicion</span>
            <span class="ti-attribute-value">{item_data.condition}</span>
        </div>
        <div class="ti-attribute">
            <span class="ti-attribute-label">Stock</span>
            <span class="ti-attribute-value">{item_data.available_quantity}</span>
        </div>
        <div class="ti-attribute">
            <span class="ti-attribute-label">Ventas</span>
            <span class="ti-attribute-value">{item_data.sold_quantity}</span>
        </div>
    </div>
    <div class="ti-actions">
        {#if !is_ours && !is_competitor}
            <button on:click={handleAddCompetitor} class="full-btn">
                <span class="material-symbols-outlined">add</span>
            </button>
        {/if}
    </div>
</div>

<style>
    .tic-trend-item {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-areas: 
            "i at at at at at ac";
        padding: var(--spacing-1) 0;
        border-bottom: 1px solid var(--primary-color);
    }

    /* .tic-trend-item * {
        border: 1px solid red;
    } */

    .ti-image {
        grid-area: i;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .ti-image a {
        width: min(150px, 30ch);
    }

    .ti-image img {
        width: 100%;
        object-fit: cover;
    }

    .ti-attributes {
        grid-area: at;
        display: flex;
        gap: 2%;
        justify-content: center;
        align-items: center;
    }

    .ti-attribute {
        width: 13%;
        text-transform: lowercase;
    }

    .ti-name {
        width: 40%;
    }

    .ti-attribute-label {
        text-transform: uppercase;
        color: var(--dark-light-color);
    }

    .ti-attribute-label::after {
        content: ": ";
    }

    .ti-attribute-value {
        color: var(--primary-color);
    }

    .ti-attribute-value-ours {
        color: var(--ready);
    }

    .ti-attribute-value-competitor {
        color: var(--danger);
    }

    .ti-actions {
        grid-area: ac;
        display: flex;
        gap: var(--spacing-1);
        justify-content: center;
        align-items: center;
    }
</style>