<script>
    import Input from "../../../components/Input/Input.svelte";
    import { KeywordFilter } from '../../../libs/dandelion-utils';
    import FieldData from "../../../libs/FieldData";

    let filter_add_field = new FieldData("filter-add-field", /.*/, "search-filtros");
    filter_add_field.placeholder = "filtro1, filtro2, filtro3...filtroN";

    export let filters = [];

    const parseFilters = () => {
        /* 
            Gets the value in filter_add_field.getFieldValue() and splits it by '\s?,\s?' regex
            and sets the resulting array to filters
        */
        let filters_string = filter_add_field.getFieldValue();
        filters = filters_string.split(/\s?,\s?/);

        if (filters.length === 1 && filters[0] === "") {
            filters = [];
        }
        filters = filters.map((filter) => new KeywordFilter(filter.split("|")));

        console.log(filters);
    };

</script>

<div id="filters-component-wrapper">
    <div id="fcw-filters-input-wrapper">
        <Input 
            field_data={filter_add_field}
            onEnterPressed={parseFilters}
            onBlur={parseFilters}
            font_size="var(--font-size-1)"
            input_background="var(--clear-color)"
            input_padding="calc(var(--spacing-1)*.6) var(--spacing-2)"
        />
    </div>
    <div id="filters-container">
        {#each filters as filter}
            <div class="fcw-fc-filter">
                {filter}
            </div>
        {/each}
    </div>
</div>

<style>
    #filters-component-wrapper {
        width: 100%;
        height: clamp(var(--spacing-4), 30%, var(--spacing-h3));
    }

    #fcw-filters-input-wrapper {
        margin-bottom: var(--spacing-2);
    }

    #filters-container {
        display: flex;
        gap: var(--spacing-2);
    }

    .fcw-fc-filter {
        box-sizing: border-box;
        cursor: default;
        min-width: calc(var(--spacing-4)*.8);
        text-align: center;
        background-color: var(--secondary-color-light);
        border-radius: var(--boxes-roundness);
        box-shadow: var(--boxes-shadow);
        color: var(--clear-color);
        padding: calc(var(--spacing-1)) ;
    }
</style>