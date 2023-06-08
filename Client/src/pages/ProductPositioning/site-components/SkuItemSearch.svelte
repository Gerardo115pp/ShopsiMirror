<script>

    import FieldData from "../../../libs/FieldData";
    import Input from "../../../components/Input/Input.svelte";
    import { onMount } from "svelte";
    import { GetMatchingProductsRequest } from '../../../libs/HttpRequests';
    import { newNotification } from '../../../components/notifications/events';
    import bonhart_storage from "../../../libs/bonhart-storage";
    import { logout } from '../../../libs/dandelion-utils';
    
    export let current_product = {};
    
    let sku_field = new FieldData("sku-field", /[A-Z\d]{1,20}/, "sku");
    let current_sku = "";

    const handleSkuField = e => {
        if (current_sku === sku_field.getFieldValue()) {
            return;
        }
        current_sku = sku_field.getFieldValue().toUpperCase();
        sku_field.setFieldValue(current_sku);
        const get_element_request = new GetMatchingProductsRequest(bonhart_storage.Token);
        get_element_request.setField("sku", current_sku);
        get_element_request.setField("competes_with", ""); // if a product has competes_with empty it means is one of our products
        
        const on_success = matching_products => {
            if (matching_products.length !== 1 && matching_products.length > 0) {
                newNotification("Aparentemente hay mas de un producto con este sku, por favor reporta este error");
                return;
            }

            current_product = matching_products[0];
        }

        const on_error = error_code => {
            switch (error_code) {
                case 401:
                    logout();
                    break;
                case 403:
                    newNotification("Parece que alguien esta haciendo algo raro, este incidente sera reportado");
                    break;
                default:
                    newNotification(`Ocurrio un error desconocido, reporta el siguiente codigo: ${error_code}`);
                    break;
            }
        }

        get_element_request.do(on_success, on_error);
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

<style>
    #sku-input-wrapper {
        padding: 0 var(--spacing-2);
    }
</style>