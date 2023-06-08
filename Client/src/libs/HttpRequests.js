import { createUnsecureJWT } from "./dandelion-utils";

export const products_server = PRODUCT_SERVER;
export const auth_server = AUTH_SERVER;
export const oauth_service = OAUTH_SERVICE;
export const events_service = EVENTS_SERVICE;

function attributesToJson() {
    const json_data = {};
    console.log("AttributestoJson:" + this);
    Object.entries(this).forEach(([key, value]) => {
        if (!(this[key] instanceof Function) && key[0] !== '_') {
            json_data[key] = value;
        }
    });
    return JSON.stringify(json_data);
}

export class CreateUserRequest {
    constructor(token) {
        this._token = token; 
        this.username = "";
        this.password = "";
        this.email = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        headers.append("Authorization", `Bearer ${this._token}`);

        const request = new Request(`${auth_server}/users`, {method: 'POST', headers: headers, body: this.toJson()});
        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    return on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetOurProductsRequest {
    constructor(token) {
        this.token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request = new Request(`${products_server}/products/ours`,{ method: 'GET', headers: headers });
        fetch(request)
            .then(promise => {
                if (promise.status >= 200 && promise.status < 300) {
                    promise.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(promise.status);
                }
            })
            
    }
}

export class LoginRequest {
    constructor() {
        this.username = "";
        this.password = "";
    }

    toJson = attributesToJson.bind(this);

    do = callback => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        const request = new Request(`${auth_server}/tokens`, {
            method: 'POST',
            headers: headers,
            body: this.toJson()
        });

        fetch(request).then(promise => {
            callback(promise);
        });
    }
}

export class GetAllUsersRequest {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${auth_server}/users`, {
            method: 'GET',
            headers: headers
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                promise.json().then(data => {
                    on_success(data);
                });
            } else {
                on_error(promise.status);
            }
        });
    }
}

export class DeleteUserRequest {
    constructor(token) {
        this._token = token;
        this.email = "";
        this.username = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${auth_server}/users`, {
            method: 'DELETE',
            headers: headers,
            body: this.toJson()
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                on_success();
            } else {
                on_error(promise.status);
            }
        });
    }               
}

export class PatchUserRequest {
    constructor(token) {
        this._token = token;
        this.id = "";
        this.email = "";
        this.username = "";
        this.password = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${auth_server}/users`, {
            method: 'PATCH',
            headers: headers,
            body: this.toJson()
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                on_success();
            } else {
                on_error(promise.status);
            }
        });
    }               

}

export class ProductsSearchRequest {
    constructor(token) {
        this.token = token;
        this.search_query = "";
        this.limit = -1;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request = new Request(`${products_server}/items/search?query=${this.search_query.replace(/\s/g, "%20")}&limit=${this.limit}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetOurProductsDataRequest {
    constructor(token) {
        this.token = token;
        this.request_fields = [];
    }

    get Fields() {
        return this.request_fields;
    }

    set Fields(field) {
        this.request_fields.push(field);
    }

    toJson = attributesToJson.bind(this);

    #composeUrl = () => {
        let url = `${products_server}/products/products_data/ours?`;
        this.request_fields.forEach(field => {
            url += `${field}=1&`;
        });
        url = url.slice(0, -1);
        return url;
    }

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request_url = this.#composeUrl();

        const request = new Request(request_url, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetMatchingProductsRequest {
    constructor(token) {
        this._token = token;
        this.search_fields = []; // a list of key-value pairs that will be matched by the returned products
    }

    toJson = attributesToJson.bind(this);

    setField = (key, value) => {
        this.search_fields.push({key: key, value: value});
    }

    getSearchUri = () => {
        let uri = `${products_server}/products/products_data/match?`;
        this.search_fields.forEach(field => {
            uri += `${field.key}=${field.value}&`;
        });
        uri = uri.slice(0, -1);
        return uri;
    }

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(this.getSearchUri(), {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class PostCompetitorProductRequest {
    constructor(token) {
        this._token = token;
        this.item_data = {};
        this.competes_with = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/`, {
            method: 'POST',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class PostOwnerProductRequest {
    constructor(token) {
        this._token = token;
        this.item_data = {};
        this.sku = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/ours`, {
            method: 'POST',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class DeleteProductRequest {
    constructor(token) {
        this._token = token;
        this.product_id = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/`, {
            method: 'DELETE',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetProductCompetitorsRequest {
    constructor(token) {
        this._token = token;
        this.product_id = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/competitors?product_id=${this.product_id}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetMeliOauthUrlRequest {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${oauth_service}/auth-url`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetCategoryTrendsRequest {
    constructor(token, category_id) {
        this._token = token;
        this.category_id = category_id;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/categories/trends?category_id=${this.category_id}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class CreateCustomQueryRequest {
    constructor(token) {
        this._token = token;
        this.keyword = "";
        this.meli_id = "";
        this.sku = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/custom-queries/`, {
            method: 'POST',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetProductCustomQueriesRequest {
    constructor(token) {
        this._token = token;
        this.sku = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/custom-queries/product?sku=${this.sku}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class DeleteCustomQueryRequest {
    constructor(token) {
        this._token = token;
        this.keyword = "";
        this.sku = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/custom-queries/`, {
            method: 'DELETE',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetReportsList {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/reports/list`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class RequestProductPerformanceReportFile {
    constructor(token) {
        this.token = token;
        this.serial = 1;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request = new Request(`${products_server}/reports/excel?serial=${this.serial}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                const header = promise.headers.get('Content-Disposition');
                const filename = header.split('=')[1];
                promise.blob().then(blob => {
                    on_success(blob, filename);
                });
            } else {
                on_error(promise.status);
            }
        });
    }
}

export class GetLatestPerformanceRecords {
    constructor(token) {
        this.token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request = new Request(`${products_server}/products/performance-records`, {
            method: 'GET',
            headers: headers
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                promise.json().then(data => {
                    on_success(data);
                });
            } else {
                on_error(promise.status);
            }
        });
    }
}

export class GetTrackedPerformanceRecords {
    constructor(token) {
        this.token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this.token}`);

        const request = new Request(`${products_server}/products/performance-records?type=tracked`, {
            method: 'GET',
            headers: headers
        });

        fetch(request).then(promise => {
            if (promise.status >= 200 && promise.status < 300) {
                promise.json().then(data => {
                    on_success(data);
                });
            } else {
                on_error(promise.status);
            }
        });
    }
}

export class GetRapidReport {
    constructor(token) {
        this._token = token;
        this.report_id = "";
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/reports/rapid-report-download?report_id=${this.report_id}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    const header = response.headers.get('Content-Disposition');
                    const filename = header.split('=')[1];
                    response.blob().then(blob => {
                        on_success(blob, filename);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

/*=============================================
=            System Events service            =
=============================================*/

export class GetSystemEventsRequest {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${events_service}/events`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetEventTypesRequest {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${events_service}/types`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

/*=====  End of System Events service  ======*/
export class GetMeliItemData {
    constructor(token, item_id, item_url) {
        this._token = token;
        this.item_id = item_id;
        this.item_url = item_url;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const jwt_params = createUnsecureJWT(this.toJson());

        const request = new Request(`${products_server}/items/item?data=${jwt_params}`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class PostTrackedProduct {
    constructor(token, item_data, sku) {
        this._token = token;
        this.item_data = item_data;
        this.sku = sku;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/track`, {
            method: 'POST',
            headers: headers,
            body: this.toJson()
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    on_success();
                } else {
                    on_error(response.status);
                }
            });
    }
}

export class GetTrackedProducts {
    constructor(token) {
        this._token = token;
    }

    toJson = attributesToJson.bind(this);

    do = (on_success, on_error) => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', `Bearer ${this._token}`);

        const request = new Request(`${products_server}/products/track`, {
            method: 'GET',
            headers: headers
        });

        fetch(request)
            .then(response => {
                if (response.status >= 200 && response.status < 300) {
                    response.json().then(data => {
                        on_success(data);
                    });
                } else {
                    on_error(response.status);
                }
            });
    }
} 