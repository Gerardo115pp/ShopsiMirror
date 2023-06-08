export const critical_events = new Set([
    "product_competitor_price_drop",
    "product_positioning_changed",
    "user_updated",
    "user_deleted",
    "user_logout"
])

export const important_events = new Set([
    "product_added",
    "user_created",
    "deleted_custom_query",
    "products_database_status_updated",
    "performance_report_started",
    "product_updated"
]);

export const info_events = new Set([
    "user_login",
    "created_custom_query",
    "product_search_performed",
    "product_competitors_updated",
    "performance_report_finished",
    "rapid_report_requested",
    "rapid_report_created"
]);