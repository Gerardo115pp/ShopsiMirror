<script>
    import FieldData from '../../libs/FieldData';
    import { FieldStates } from '../../libs/FieldData';
    import { onMount } from 'svelte';

    // Styles
    export let isClear = false;
    export let isSquared = false;

    export let field_data = new FieldData("generic-input", /[.\n]+/, "any"); 
    export let input_label;
    export let show_placeholder = false;
    export let input_padding = "var(--spacing-2) var(--spacing-2)";
    export let input_background = "none";
    export let onKeypressed;
    export let onEnterPressed;
    export let onBlur;

    /* CSS variables */
    export let input_color = "var(--primary-color)";
    export let input_dark_color = "var(--dark-light-color)";
    export let border_color = "var(--primary-color)";
    export let title_font = "var(--font-title)";
    export let text_font = "var(--font-text)";
    export let font_size = "var(--font-size-2)";

    export let initial_value;
    export let min = 0;
    export let max;
    export let autocomplete = "off";

    $: state_color = getBorderColor(field_data.state) ;

    let button_pointer = undefined;

    onMount(() => {
        setCssVariables();
    })

    const awaitKeys = e => {
        if (e.key.toLowerCase() === 'enter' && onEnterPressed !== undefined) {

            field_data.getField().blur();
            return onEnterPressed(e);
            
        } else if (onKeypressed !== undefined) {
            
            return onKeypressed(e);
        }
    }

    const handleOutsideClickDetected = e => {
        if(e.currentTarget === e.target) {
            e.target.getElementsByTagName("input")[0].focus()
        }
    }

    const getBorderColor = state => {
        switch(state) {
            case FieldStates.NORMAL:
                return "--libery-input-dark-color";
            case FieldStates.HAS_ERRORS:
                return "--danger";
            case FieldStates.READY:
                return "--ready";
            default:
                return "--libery-input-dark-color"
        }
    }

    const composeClassName = () => {
        let class_name = "input-container";

        class_name += isSquared ? " squared" : "";

        if(isClear) {
            class_name += " clear-input";
        }
        return class_name;
    }

    const setCssVariables = () => {
        let input = document.querySelector(":root");    
        
        input.style.setProperty("--libery-input-color", input_color);
        input.style.setProperty("--libery-input-dark-color", input_dark_color);
        input.style.setProperty("--libery-input-border-color", border_color);
        input.style.setProperty("--libery-input-title-font", title_font);
        input.style.setProperty("--libery-input-text-font", text_font);
    }

</script>

<style>
    .input-container {
        box-sizing: border-box;
        cursor: text;
        width: 100%;
        display: flex;
        border: 2px solid var(--libery-input-border-color);
        border-radius: 9999px;
        align-items: center;
    }   

    .input-container label {
        font-family: var(--libery-input-title-font);
        color: var(--libery-input-dark-color);
        width: max-content;
        margin-left: 1vw;
        text-transform: capitalize;
        white-space: nowrap;
    }

    .input-container input {
        font-family: var(--libery-input-text-font);
        width: 100%;
        display: flex;
        background: none;
        border: none;
        color: var(--libery-input-color);
        padding: 0;
        align-items: center;
        outline: none;
    }

    .input-container input[type='number'] {
        width: 5rem;
        text-align: center;
        -moz-appearance: textfield;
        appearance: textfield;
    }

    .input-container input::placeholder {
        font-family: var(--libery-input-text-font);
        color: var(--placeholder-color);
        text-transform: unset;
    }

    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
    }

    .input-container.clear-input {
        border: none;
        border-bottom: 2px solid var(--libery-input-dark-color);
        border-radius: 0 !important;
        flex-direction: column;
    }

    .input-container.clear-input > label {
        display: block;
        margin-left: -2vw;
        color: var(--libery-input-dark-color);
        font-weight: regular;
        align-self: flex-start;
    }

    .input-container > input[type='password'] {
        letter-spacing: .5em;
    }

    .input-container > input[type='password']::placeholder {
        letter-spacing: 0.4px;
    }


    .input-container.squared {
        border-radius: 5px;
    }
</style>

<div 
    bind:this={button_pointer} 
    on:click={handleOutsideClickDetected}
    style="padding: {input_padding};border-color: var({state_color}); background: {input_background};" 
    class={composeClassName()}
>
    {#if input_label !== undefined}
        <label style="font-size: {font_size};"  for={field_data.id}>{input_label}</label>
    {/if}
    {#if field_data.type !== "number"}
        <input id={field_data.id} type={field_data.type}
            placeholder={input_label === undefined || show_placeholder ? field_data.placeholder : ""}
            style="margin: {input_padding}; font-size: {font_size};"
            on:keydown={awaitKeys}
            on:blur={onBlur}
        />
    {:else}
        <input id={field_data.id} type={field_data.type}
            placeholder={input_label === undefined ? field_data.placeholder : ""}
            on:keydown={awaitKeys}
            on:blur={onBlur}
            value={initial_value}
            style="font-size: {font_size};"
            min={min}
            max={max}
            autocomplete="{autocomplete}"
        />
    {/if}

</div>