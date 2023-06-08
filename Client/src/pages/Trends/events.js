export const trends_events = {
    TREND_KEYWORD_SELECTED: 'trend_option_selected',
    TREND_ITEM_COMPETES: 'trend_item_competes'
}

export const emitTrendKeywordSelected = trend_keyword => {
    const event = new CustomEvent(trends_events.TREND_KEYWORD_SELECTED, { detail: trend_keyword });
    document.dispatchEvent(event);
}

export const emitTrendItemCompetes = trend_item => {
    const event = new CustomEvent(trends_events.TREND_ITEM_COMPETES, { detail: trend_item });
    document.dispatchEvent(event);
}