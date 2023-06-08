<script>
        import { routes } from "./routes";
        import Router from "svelte-spa-router";
        import Navbar from "./components/Navbar/Navbar.svelte";
        import NotificationsPopup from "./components/notifications/NotificationsPopup.svelte";

</script>

<style>


    :global(:root) {
        /* Colors */
        --primary-color: #3D50FC;
        --secondary-color: #5F4CFD;
        --tertiary-color: #3D50FC;
        --primary-color-light: #C5A3FF;
        --secondary-color-light: #A095FF;
        --tertiary-color-light: #A1ABFF;
        --primary-color-midlight: #A671FF;
        --secondary-color-midlight: #8172FF;
        --tertiary-color-midlight: #6675FF;
        --primary-color-dark: #280742;
        --secondary-color-dark: #1f004d;
        --dark-light-color: #00000080;
        --placeholder-color: #00000025;
        --grey-color: rgba(113, 113, 113, 0.539);
        --danger: #d33434;
        --danger-light: #e25252;
        --ready: #3dfcbc;
        --clear-color: #FFFFFF;
        --clear-theme-color: #d7dbff;
        --dark-color: var(--primary-color-dark);
        --dark-tranparent-background: rgba(0, 0, 0, 0.3);
        
        /* Fonts */
        --primary-font: 'Exo 2', sans-serif;
        --font-title: var(--primary-font);
        --font-text: var(--primary-font);

        --font-size-1: 2.2257405515832482vh;
        --font-size-2: calc(var(--font-size-1) + calc(var(--font-size-1) * 0.55));
        --font-size-3: calc(var(--font-size-1) + calc(var(--font-size-1) * 0.7));
        --font-size-4: calc(var(--font-size-1) + calc(var(--font-size-1) * 1.1));
        --font-size-h1: calc(var(--font-size-1) * 5.5);
        --font-size-h2: calc(var(--font-size-h1) * 0.80);
        --font-size-h3: calc(var(--font-size-h1) * 0.6);
        --font-size-h4: calc(var(--font-size-h1) * 0.4);
        --font-size-small: calc(var(--font-size-1) * 0.8);
        
        font-size: var(--font-size-1);
        
        /* Spacing */

        --spacing-1: 0.8vh;
        --spacing-2: calc(var(--spacing-1) * 2);
        --spacing-3: calc(var(--spacing-2) * 2.5);
        --spacing-4: calc(var(--spacing-3) * 3.5);
        --spacing-h1: calc(var(--spacing-4) * 4);
        --spacing-h2: calc(var(--spacing-h1) * 0.75);
        --spacing-h3: calc(var(--spacing-h1) * 0.5);
        --spacing-h4: calc(var(--spacing-h1) * 0.25);

        --primary-gradient: linear-gradient(115deg, rgba(61,80,252,1) 0%, rgba(95,76,253,1) 53%, rgba(124,57,237,1) 100%);
        --boxes-roundness: 13px;
        --navbar-height: calc(var(--spacing-3) *2);
        --boxes-shadow: 0px 5px 4px 1px rgba(0, 0, 0, 0.1);
        --boxes-shadow-2: 0px 5px 20px 8px rgba(0, 0, 0, 0.2);
        --inset-shadow: inset 0px 0px 10px 3px rgba(0, 0, 0, 0.1);
        --inset-shadow-2: inset 0px 0px 10px 3px rgba(0, 0, 0, 0.2);
        letter-spacing: var(--letter-spacing);
        
        /* buttons */
        --buttons-padding: var(--spacing-1) calc(var(--spacing-2) * 1.2);
        --buttons-text-transform: capitalize;
        --btn-font-size: var(--font-size-1);
        --button-roundness: var(--boxes-roundness);
        --button-shadow: var(--boxes-shadow);
        --button-font-weight: 500;

        /* Z-index */
        --z-index-1: 1;
        --z-index-2: 2;
        --z-index-3: 3;
        --z-index-4: 4;
        --z-index-5: 5;
        --z-index-6: 6;
        --z-index-7: 7;
        --z-index-8: 8;
        --z-index-9: 9;
        --z-index-10: 10;
    }

    :global(*) {
        box-sizing: border-box;
    }

    :global(html) {
        font-size: 2vw;
        padding: 0;
    }

    :global(body) {
        font-family: var(--primary-font);
        margin: 0;
        height: 100vh;
        border-top: 1px solid transparent;
    }

    :global(body::-webkit-scrollbar) {
        display: none;
    }

    :global(h1, h2, h3, h4, h5, h6) {
        margin: 0;
    }

    :global(.round-box) {
        border-radius: var(--boxes-roundness);
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
    }

    :global(.full-btn) {
        cursor: pointer;
        box-sizing: border-box;
        display: grid;
        place-items: center;
        padding: var(--buttons-padding);
        color: var(--clear-color);
        background-color: var(--primary-color);
        border-radius: var(--button-roundness);
        font-weight: var(--button-font-weight);
        font-size: var(--btn-font-size);
        border: none;
        box-shadow: var(--button-shadow);
        transition: all 0.3s ease-in-out;
        text-transform: var(--buttons-text-transform);
    }

    :global(.full-two-btn) {
        cursor: pointer;
        box-sizing: border-box;
        padding: var(--buttons-padding);
        color: var(--clear-color);
        background-color: var(--primary-color-light);
        border-radius: var(--button-roundness);
        font-weight: var(--button-font-weight);
        font-size: var(--btn-font-size);
        border: none;
        box-shadow: var(--button-shadow);
        transition: all 0.3s ease-in-out;
        text-transform: var(--buttons-text-transform);
    }

    :global(.clear-btn) {
        cursor: pointer;
        box-sizing: border-box;
        background-color: rgba(255, 255, 255, 0.658);
        color: var(--primary-color-dark);
        border: 1px solid var(--dark-color);
        padding: 0.5em 2em;
        border-radius: var(--button-roundness);
        font-weight: var(--button-font-weight);
        font-size: var(--btn-font-size);
        box-shadow: var(--button-shadow);
        transition: all 0.2s ease-in;
        text-transform: var(--buttons-text-transform);
    }

    :global(.danger-btn) {
        cursor: pointer;
        box-sizing: border-box;
        background-color: var(--danger);
        color: var(--clear-color);
        border: none;
        padding: var(--buttons-padding);
        border-radius: var(--button-roundness);
        font-weight: var(--button-font-weight);
        font-size: var(--btn-font-size);
        box-shadow: var(--button-shadow);
        transition: all 0.2s ease-in;
        text-transform: var(--buttons-text-transform);
    }

    :global(.page-title) {
        font-size: var(--font-size-2);
        font-weight: 500;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
    }

    #content-wrap {
        margin-top: calc(var(--navbar-height) + var(--spacing-2));
    }

    :global(.highlighted-text){
        color: var(--primary-color);
    }

    @media (pointer: fine) {
        :global(.clear-btn:hover) {
            background-color: var(--primary-color);
            color: var(--dark-color);
            /* border: none; */
        }

        :global(.full-btn:hover) {
            background-color: var(--primary-color-light);
            color: var(--clear-color);
            transform: scale(1.1);
            box-shadow: 0px 5px 8px 3px rgba(0, 0, 0, 0.18);
        }

        :global(.full-two-btn:hover) {
            background-color: var(--primary-color-midlight);
            color: var(--clear-color);
            transform: scale(1.1);
            box-shadow: 0px 5px 8px 3px rgba(0, 0, 0, 0.18);
        }

        :global(.danger-btn:hover) {
            background-color: var(--danger-light);
            color: var(--clear-color);
            transform: scale(1.1);
            box-shadow: 0px 5px 8px 3px rgba(0, 0, 0, 0.18);
        }
    }

    
    /*=============================================
    =            Animations            =
    =============================================*/
    
    @keyframes slide-fwd-bottom {
        0% {
            -webkit-transform: translateZ(160px) translateY(-100px);
                    transform: translateZ(160px) translateY(-100px);
        }
        100% {
            -webkit-transform: translateZ(0) translateY(0);
                    transform: translateZ(0) translateY(0);
        }
    }

    :global(.slide-fwd-bottom) {
        -webkit-animation: slide-fwd-bottom 0.45s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
        animation: slide-fwd-bottom 0.45s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
    }

    @keyframes blink-1 {
        0%,
        50%,
        100% {
            opacity: 1;
        }
        25%,
        75% {
            opacity: 0;
        }
    }

    :global(.blink-1) {
        -webkit-animation: blink-1 .5s ease-in-out infinite both;
        animation: blink-1 .5s ease-in-out infinite both;
    }
    
    /*=====  End of Animations  ======*/
    
    
</style>


<svelte:head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</svelte:head>
<div id="page-content">
    <NotificationsPopup />
    <Navbar />
    <div id="content-wrap">
        <Router {routes} />
    </div>
</div>