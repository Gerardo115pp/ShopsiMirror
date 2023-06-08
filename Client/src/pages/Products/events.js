export const products_events = {
    TIME_RANGE_CHANGED: 'time_range_changed'
}

export const emitTimeRangeChanged = time_range => {
    const event = new CustomEvent(products_events.TIME_RANGE_CHANGED, { detail: time_range });
    document.dispatchEvent(event);
}