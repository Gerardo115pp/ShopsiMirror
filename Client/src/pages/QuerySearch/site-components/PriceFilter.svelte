<script>
    import FieldData from "../../../libs/FieldData";
    import Input from "../../../components/Input/Input.svelte";
    import newNotification from '../../../components/notifications/events';
    import {PriceRange} from '../../../libs/dandelion-utils';

    export let price_range = new PriceRange(0, Infinity);

    let price_range_field = new FieldData("price-range-field", /[\d\-\.\s]*/, "price_range");

    const prasePriceRange = () => {
        const price_range_string = price_range_field.getFieldValue();
        const price_range_array = price_range_string.split("-").map(price => Number(price.trim()));
        if (price_range_array.length === 2 && !isNaN(price_range_array[0]) && !isNaN(price_range_array[1])) {
            price_range = new PriceRange(price_range_array[0], price_range_array[1]);
        } else {
            newNotification(`El formato de rango de precio '${price_range_string}' no es válido.`);
            resetPriceRange();
        }
    }

    const resetPriceRange = () => {
        price_range_field.clear();
        price_range = new PriceRange(0, Infinity);
    }
</script>

<div id="price-range-input-wrapper">
    <Input
        field_data={price_range_field}
        onEnterPressed={prasePriceRange}
        onBlur={prasePriceRange}
        input_label="rango de precio"
        font_size="var(--font-size-small)"
        input_background="var(--clear-color)"
        input_padding="calc(var(--spacing-1)*.6) var(--spacing-1)"
    />
</div>