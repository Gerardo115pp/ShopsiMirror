<script>
    import { newNotification } from "../../../components/notifications/events";
    import { CreateCustomQueryRequest } from "../../../libs/HttpRequests";
    import FieldData, { FieldStates } from "../../../libs/FieldData";
    import Input from "../../../components/Input/Input.svelte";
    import bonhart_storage from "../../../libs/bonhart-storage";
    import { emitCustomQuerysChanged } from "../events";

    export let target_product = undefined;
    let is_enabled = true;
    $: is_enabled = target_product !== undefined;

    let custom_search_query = undefined;
    
    const queryCreatorField = new FieldData("query_creator", /.{3,}/, "query_creator");
    queryCreatorField.placeholder = "Crea un termino de busqueda, 3+ caracteres";

    const hanldeCreateQuery = () => {
        if (!is_enabled) {
            newNotification("Para crear un termino de busqueda, primero selecciona un producto en el campo de sku");
            return;
        }

        if (!queryCreatorField.isReady()) {
            newNotification("El termino de busqueda no puede estar vacio y debe tener al menos 3 caracteres");
            return;
        }

        custom_search_query = queryCreatorField.getFieldValue();
        const create_query_request = new CreateCustomQueryRequest(bonhart_storage.Token);
        create_query_request.sku = target_product.sku;
        create_query_request.keyword = custom_search_query;
        create_query_request.meli_id = target_product.meli_id;
        
        if (create_query_request.keyword === "" || create_query_request.sku === "") {
            newNotification("El termino de busqueda y el sku no pueden estar vacios");
            return;
        }
        
        const on_success = () => {
            newNotification(`Termino de busqueda creado: ${custom_search_query}`);
            queryCreatorField.clear();
            emitCustomQuerysChanged();
        };

        const on_error = (error) => {
            newNotification(`Error al crear el termino de busqueda: ${error}`);
        };

        create_query_request.do(on_success, on_error);
    }
</script>

<div id="ppp-query-creator-wrapper">
    <div id="ppp-qcw-input-wrapper">
        <Input
            field_data={queryCreatorField}
            font_size="var(--font-size-1)"
            input_background="var(--clear-color)"
            input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
        />
    </div>
    <div id="ppp-qcw-create-btn">
        <button on:click={hanldeCreateQuery} class="full-btn">
            <span class="material-symbols-outlined">create</span>
        </button>
    </div>
</div>

<style>

    #ppp-query-creator-wrapper {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
    }

    #ppp-qcw-input-wrapper {
        grid-column: 1 / 5;
        padding: 0 var(--spacing-2);
    }

    #ppp-qcw-create-btn {
        display: grid;
        grid-column: 5 / 6;
        place-items: center;
    }
</style>