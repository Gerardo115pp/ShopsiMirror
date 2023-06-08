export const product_detail_events = {
    DELETED_COMPETITOR: 'deleted_competitor'
}

export const emitDeletedCompetitor = (competitor) => {
    const event = new CustomEvent(product_detail_events.DELETED_COMPETITOR, { detail: competitor });
    document.dispatchEvent(event);
}