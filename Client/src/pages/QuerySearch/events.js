export const query_search_events = {
    SKU_CHANGED: 'sku_changed'
}

export const emitSkuChanged = sku => {
    const event = new CustomEvent(query_search_events.SKU_CHANGED, { detail: sku });
    document.dispatchEvent(event);
}