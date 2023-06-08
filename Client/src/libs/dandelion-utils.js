import { push } from 'svelte-spa-router';   
import bonhart_storage from './bonhart-storage';

const SHOPSI_TOKEN = "shopsi-token"; // cookie name

export const isLoggedIn = (redirect=true) => {
    let json_web_token = bonhart_storage.Token;
    console.log("isLoggedIn", json_web_token);

    let is_logged_in = json_web_token !== "";

    if (!is_logged_in && redirect) {
        alert("You must be logged in to access this page.");
        push("/login");
    }

    return is_logged_in;
}

export const logout = () => {
    bonhart_storage.Token = "";
    push("/login");
}

export const getThumbnailId = thumbnail_url => {
    /* 
        a thumbnail id looks like this: 644093-MLM46303604177_062021
        and the thumbnail url looks like this: https://http2.mlstatic.com/D_644093-MLM46303604177_062021-O.webp
    */
    const thumbnail_id_regex = /\d{6}-[A-Z]{3}\d{11}_\d{6}/g;
    const matches = thumbnail_id_regex.exec(thumbnail_url);
    if (matches) {
        return matches[0];
    }
    return null;
}
window.getThumbnailId = getThumbnailId;

export const getMeliIdFromUrl = url => {
    const meli_id_regex = /[A-z]{2,3}-?\d{6,14}/g;
    const matches = meli_id_regex.exec(url);
    if (matches) {
        return matches[0];
    }
    return null;
}

export const createUnsecureJWT = payload => {
    /* 
        Keep in mind that this method of creating a JWT is not secure, as the JWT is not signed and could be easily tampered with. It is only suitable for passing simple parameters that do not need to be secured.
    */

    const headers = {
        alg: "none",
        typ: "JWT"
    }

    const encoded_headers = window.btoa(JSON.stringify(headers)); // stupid vscode doesnt relize we are not working in node but in the browser

    const encoded_payload = window.btoa(JSON.stringify(payload));

    return `${encoded_headers}.${encoded_payload}.`;
}

export class PriceRange {
    #min
    #max

    constructor(min, max) {
        this.#min = min;
        this.#max = max;
        if (this.#min > this.#max) {
            throw new Error("min price cannot be greater than max price");
        }
    }

    get Min() {
        return this.#min;
    }

    get Max() {
        return this.#max;
    }

    clamp = (price) => {
        if (price < this.#min) {
            return this.#min;
        } else if (price > this.#max) {
            return this.#max;
        } else {
            return price;
        }
    }

    inRange = (price) => {
        return price >= this.#min && price <= this.#max;
    }


}

export class KeywordFilter {
    constructor(keywords) {
        this.keywords = this.#transform(keywords);
    }

    #transform = keywords => {
        let transformed_keywords = [];
        if (keywords === "") {
            return transformed_keywords;
        }

        if (!Array.isArray(keywords)) {
            keywords = [keywords];
        }

        for (let keyword of keywords) {
            transformed_keywords.push(keyword.trim().toLowerCase());
        }

        return transformed_keywords;
    }

    match = text => {
        let match_any = this.keywords.reduce((acc, keyword) => {
            let match = text.toLowerCase().includes(keyword);
            console.log(`keyword: ${keyword}, match: ${match}, previous: ${acc}`);
            return acc || match;
        }, false);

        return match_any;
    }

    toString = () => {
        // wrap each keyword in quotes and join them with a ' or '
        return this.keywords.map(keyword => `"${keyword}"`).join(" or ");
    }
}