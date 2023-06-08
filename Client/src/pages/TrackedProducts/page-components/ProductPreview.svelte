<script>
    export let item_data;

    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 3
    });

</script>

<div id="tpp-new-product-preview">
    <div id="tpp-npp-preview-image-wrapper">
        <img src={item_data.secure_thumbnail} alt={item_data.title} />
    </div>
    <div id="tpp-npp-product-name-wrapper">
        <h3>{item_data.title}</h3>
    </div>
    <div id="tpp-npp-product-data-wrapper">
        <div class="pdw-product-data" id="pdw-price">
            <span class="pdw-data-name">precio</span>
            <span class="pdw-data-value">{item_data.price !== undefined ? price_formatter.format(item_data.price) : "?"}</span>
        </div>
        <div class="pdw-product-data" id="pdw-quantity">
            <span class="pdw-data-name">cantidad</span>
            <span class="pdw-data-value">{item_data.available_quantity !== undefined ? item_data.available_quantity : "?"}</span>
        </div>
        <div class="pdw-product-data" id="pdw-status">
            <span class="pdw-data-name">estado</span>
            <span class="pdw-data-value">{item_data.status !== undefined ? item_data.status : "?"}</span>
        </div>
        <div class="pdw-product-data" id="pdw-condicion">
            <span class="pdw-data-name">condicion</span>
            <span class="pdw-data-value">{item_data.condition !== undefined ? item_data.condition : "?"}</span>
        </div>
    </div>
</div>

<style>

    #tpp-new-product-preview {
        display: grid;
        width: 100%;
        grid-template-columns: repeat(4, 1fr);
        gap: var(--spacing-1);
    }

    #tpp-npp-preview-image-wrapper {
        grid-column: 1 / 2;
        grid-row: 1 / 3;
    }

    #tpp-npp-product-name-wrapper {
        grid-column: 2 / 5;
    }

    #tpp-npp-product-data-wrapper {
        grid-column: 2 / 5;
        grid-row: 2 / 3;
        display: flex;
        gap: var(--spacing-3);
    }

    .pdw-product-data {
        font-size: var(--font-size-small);
    }

    .pdw-data-name {
        color: var(--primary-color);
    }

    .pdw-data-name::after {
        content: ":";
    }

</style>