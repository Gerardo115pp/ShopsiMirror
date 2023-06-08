export const product_positioning_events = {
    CUSTOM_QUERY_SELECTED: 'custom_query_selected',
    CUSTOME_QUERYS_CHANGED: 'custom_querys_changed',
    PRODUCT_COMPETES: 'product_competes'
}

export const emitCustomQuerySelected = custom_query => {
    const event = new CustomEvent(product_positioning_events.CUSTOM_QUERY_SELECTED, { detail: custom_query });
    document.dispatchEvent(event);
}

export const emitCustomQuerysChanged = () => {
    const event = new CustomEvent(product_positioning_events.CUSTOME_QUERYS_CHANGED);
    document.dispatchEvent(event);
}

export const emitProductCompetes = product => {
    const event = new CustomEvent(product_positioning_events.PRODUCT_COMPETES, { detail: product });
    document.dispatchEvent(event);
}