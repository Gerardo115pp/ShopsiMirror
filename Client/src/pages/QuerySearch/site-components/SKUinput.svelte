<script>

    import FieldData from "../../../libs/FieldData";
    import Input from "../../../components/Input/Input.svelte";
    import { onMount, onDestroy } from "svelte";
    import { GetOurProductsDataRequest } from '../../../libs/HttpRequests';
    import { newNotification } from '../../../components/notifications/events';
    import bonhart_storage from "../../../libs/bonhart-storage";
    import { query_search_events } from '../events';
    import { logout } from '../../../libs/dandelion-utils';

    let sku_field = new FieldData("sku-field", /[A-Z\d]{1,20}/, "sku");
    
    export let current_sku = "";
    export let current_product_id = "";
    export let create_product_mode = false;
    export let exiting_skus = []; // Array of object with {sku: "sku", name: "name", product_id: "product_id"}

    onMount(() => {
        if (exiting_skus.length === 0) {
            requestProductsSkus();
        }

        document.addEventListener(query_search_events.SKU_CHANGED, requestProductsSkus);
    });

    onDestroy(() => {
        document.removeEventListener(query_search_events.SKU_CHANGED, requestProductsSkus);
    });

    const requestProductsSkus = () => {
        const product_skus_request = new GetOurProductsDataRequest(bonhart_storage.Token);
        product_skus_request.Fields = "sku"
        product_skus_request.Fields = "name"

        const on_error = (http_error_code) => {
            if (http_error_code === 401) {
                newNotification("Parece que tu sesión ha expirado, por favor vuelve a iniciar sesión");
                logout();
                return;
            }

            newNotification(`Error ${http_error_code} al obtener los skus, favor de reportarlo`);
        }

        const on_success = response_data => {
            sku_field.clear();
            current_sku = "";
            current_product_id = "";
            create_product_mode = false;
            exiting_skus = response_data;
        }

        product_skus_request.do(on_success, on_error);
    }

    const handleSkuField = e => {
        const sku = sku_field.getFieldValue();
        if (sku.length > 0) {
            console.log(sku);
            const sku_object = exiting_skus.find(sku_object => sku_object.sku === sku);
            if (sku_object) {
                current_sku = sku_object.sku;
                current_product_id = sku_object.product_id;
                create_product_mode = false;
                newNotification(`Se agregaran competencias a '${sku_object.name}'`);
            } else {
                current_sku = sku;
                create_product_mode = true;
                newNotification("SKU no encontrado, al agregar un producto propio se utlizara el SKU ingresado");
            }
        }
    }
</script>

<div id="sku-input-wrapper">
    <Input
        field_data={sku_field}
        onEnterPressed={handleSkuField}
        onBlur={handleSkuField}
        input_label="SKU"
        font_size="var(--font-size-1)"
        input_background="var(--clear-color)"
        input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
    />
</div>