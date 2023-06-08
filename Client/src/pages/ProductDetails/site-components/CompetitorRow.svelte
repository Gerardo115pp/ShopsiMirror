<script>
    import { newNotification } from '../../../components/notifications/events';
    import { DeleteProductRequest } from '../../../libs/HttpRequests';
    import { emitDeletedCompetitor } from '../events';
    import bonhart_storage from '../../../libs/bonhart-storage';

    export let competitor_data = {
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
    }

    const price_formatter = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    });

    const openProductInNewTab = () => {
        window.open(competitor_data.meli_url, '_blank');
    }

    const handleDeleteBtn = () => {
        const delete_request = new DeleteProductRequest(bonhart_storage.Token);
        delete_request.product_id = competitor_data.product_id;

        const on_success = response => {
            newNotification(`Producto ${competitor_data.meli_id} eliminado correctamente`);
            emitDeletedCompetitor(competitor_data);
        }

        const on_error = http_error_code => {
            newNotification(`Error al eliminar producto,favor de reportar: ${http_error_code}`);
        }

        delete_request.do(on_success, on_error);
    }
</script>

<div class="bonhart-competitor-row">
    <div class="bcr-product-attribute bcr-product-image">
        <img src={competitor_data.secure_thumbnail} alt={competitor_data.name}/>
    </div>
    <div class="bcr-product-attribute">
        <span class="bcr-pa-label">Nombre</span>
        <span class="bcr-pa-value">{competitor_data.name}</span>
    </div>
    <div class="bcr-product-attribute">
        <span class="bcr-pa-label">Condition</span>
        <span class="bcr-pa-value">{competitor_data.condition}</span>
    </div>
    <div class="bcr-product-attribute">
        <span class="bcr-pa-label">Estado</span>
        <span class="bcr-pa-value">{competitor_data.status}</span>
    </div>
    <div class="bcr-product-attribute">
        <span class="bcr-pa-label">Precio</span>
        <span class="bcr-pa-value">{price_formatter.format(competitor_data.initial_price)}</span>
    </div>
    <div class="bcr-product-actions">
        <button on:click={openProductInNewTab} class="full-btn">
            <span class="material-symbols-outlined">open_in_new</span>
        </button>
        <button on:click={handleDeleteBtn}  class="danger-btn">
            <span class="material-symbols-outlined">delete</span>
        </button>
    </div>
</div>

<style>
    .bonhart-competitor-row {
        display: flex;
        gap: var(--spacing-3);
        align-items: center;
        border-bottom: 1px solid var(--primary-color);
    }
/* 
    .bonhart-competitor-row  *{
        border: 1px solid red;
    } */

    .bonhart-competitor-row:last-child {
        border-bottom: none;
    }

    .bcr-product-attribute {
        width: 18%;
        font-size: var(--font-size-small);
    }

    .bcr-product-attribute .bcr-pa-label {
        color: var(--primary-color);
    }

    .bcr-product-attribute .bcr-pa-label::after {
        content: ":";
    }

    .bcr-product-image {
        width: 8%;
    }

    .bcr-product-image img {
        width: 100%;
    }

    .bcr-product-actions {
        display: flex;
        gap: var(--spacing-1);
        width: 30%;
        justify-content: center;
    }


</style>