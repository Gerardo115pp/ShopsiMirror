export const tracked_products_events = {
    TRACKED_PRODUCTS_CHANGED: 'tracked_products_changed'
}

export const emitTrackProductsChanged = trackedProducts => {
    const event = new CustomEvent(tracked_products_events.TRACKED_PRODUCTS_CHANGED, { detail: trackedProducts });
    document.dispatchEvent(event);
}