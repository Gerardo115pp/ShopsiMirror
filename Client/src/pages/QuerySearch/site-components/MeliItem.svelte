<script>
    export let item_data;
    export let my_price;
    export let is_ours = false;
    export let is_competitor = false;
    export let is_tracked = false;
    export let create_product_mode = false;

    let show_description = false;
    export let add_competitor_callback= () => {};
    export let add_our_product_callback = () => {};
    export let add_tracked_item_callback = () => {};

    const color_classes = {
        "higher": "mic-higher-price",
        "lower": "mic-lower-price"
    }

    
    let price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    });
    
    const getColorClass = (price, other) => color_classes[price > other ? "higher" : "lower"];
    
    $: color_class = getColorClass(item_data.price, my_price);
</script>

<div  class="meli-item-container">
    <div class="meli-item-inline-content">
        <div class="mic-item-image-wrapper">
            <img src={item_data.thumbnail} alt="{item_data.name}"/>
        </div>
        <div class="mic-item-name-wrapper">
            <a rel="noopener" target="_blank" href={item_data?.url}>
                {#if is_ours}
                    <span class="mic-our-item">(tuyo)</span>
                {:else if is_competitor}
                    <span class="mic-competitor-item">(competidor)</span>
                {:else if is_tracked}
                    <span class="mic-tracked-item">(rastreado)</span>
                {/if}
                {item_data.name}
            </a>
        </div>
        <div class="mic-item-price">Precio: <span class="mic-ip-price {color_class}">{price_formatter.format(item_data.price)}</span></div>
        <div class="mic-controls-container">
            {#if (!is_ours && !is_competitor)}
                 <div on:click={() => add_competitor_callback(item_data)} class="mic-cc-control mic-cc-add-competitor full-btn">
                     <span class="material-symbols-outlined">add</span>
                 </div>
            {:else if create_product_mode}
                <div on:click={() => add_our_product_callback(item_data)} class="mic-cc-control mic-cc-add-competitor full-btn">
                    <span class="material-symbols-outlined">assignment_add</span>
                </div>
            {/if}
            {#if create_product_mode && !is_tracked}
                <div on:click={() => add_tracked_item_callback(item_data)} class="mic-cc-control mic-cc-add-competitor full-btn">
                    <span class="material-symbols-outlined">location_searching</span>
                </div>
            {/if}
            <div on:click={() => show_description = !show_description} class="mic-cc-control mic-cc-add-competitor full-btn">
                <span class="material-symbols-outlined">info</span>
            </div>
        </div>
    </div>
    {#if show_description}
         <div class="meli-item-description">
            <ul class="meli-desc-fields">
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Available: </span>
                    <span class="meli-desc-field-value">{item_data.available_quantity}</span>
                </li>
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Condition: </span>
                    <span class="meli-desc-field-value">{item_data.condition}</span>
                </li>
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Free shipping: </span>
                    <span class="meli-desc-field-value">{item_data.free_shipping}</span>
                </li>
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Location: </span>
                    <span class="meli-desc-field-value">{item_data.location}</span>
                </li>
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Original price: </span>
                    <span class="meli-desc-field-value">{item_data.original_price}</span>
                </li>
                <li class="meli-desc-field">
                    <span class="meli-desc-field-name">Attributes: </span>
                    <span class="meli-desc-field-value">{item_data.attributes}</span>
                </li>
            </ul>
         </div>
    {/if}
</div>

<style>
    .meli-item-container {
        width: 100%;
        border-bottom: 1px solid var(--secondary-color-light);
    }
    
    /* .meli-item-container * {
        border: 1px solid red;
    } */
    
    .meli-item-container:hover {
        background-color: rgb(246, 246, 255);
    }
    
    .meli-item-inline-content {
        display: flex;
        min-height: calc(var(--spacing-h3)*.8);
        justify-content: space-around;
        align-items: center;
    }

    .mic-item-name-wrapper {
        width: 44%;
        height: max-content;
    }

    .mic-item-name-wrapper a {
        display: inline-block;
        overflow: hidden;
        width: 100%;
        color: var(--primary-color-dark);
        text-decoration: none;
        font-size: var(--font-size-1);
        white-space: nowrap;
        text-overflow: ellipsis;
        margin: 0;
    }

    .mic-our-item {
        color: var(--primary-color);
    }

    .mic-competitor-item {
        color: var(--danger);
    }

    .mic-item-price {
        font-size: var(--font-size-1);
    }
    
    .mic-item-price span:global(.mic-higher-price) {
        color: #2abe71;
    }

    .mic-item-price span:global(.mic-lower-price) {
        color: #ff2a2a;
    }
    

    .mic-item-image-wrapper img {
        width: calc(var(--spacing-h4) * 1.2);
    }

    .meli-item-description {
        background: rgb(252, 249, 255);
    }

    .meli-desc-fields {
        list-style: none;
        padding: 1vh 5vw;
    }

    .meli-desc-field-name {
        font-size: var(--font-size-small);
        font-weight: bold;
        color: var(--primary-color-dark);
    }

    .meli-desc-field-value {
        font-size: var(--font-size-small);
        font-weight: lighter;
        color: var(--secondary-color-midlight);
    }

    /* Controls */

    .mic-controls-container {
        display: flex;
        justify-content: center;
        gap: var(--spacing-2);
        align-items: center;
    }

    .mic-cc-control {
        width: max-content;
        
    }
</style>