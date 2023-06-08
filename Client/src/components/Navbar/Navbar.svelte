<script>
    import { push, link } from 'svelte-spa-router';
    import DropDown from './sub-components/DropDown.svelte';
    import bonhart_storage from '../../libs/bonhart-storage';

    const shopsi_logo = "/resources/logos/logo_shopsi-M.webp";

    const logout = () => {

        bonhart_storage.Token = "";
        push('/login');
    };
</script>

<nav id="meli-mvp-header">
    <div id="mmh-navbar-container">
        <div id="mmh-navbar-logo">
            <div id="mmh-lg-logo">
                <img src="{shopsi_logo}" alt="shopsi logo">
            </div>
        </div>
        <div id="meli-mvp-options">
            <span class="meli-navoption">
                <a href="/" use:link>
                    buscador
                </a>
            </span>
            <span class="meli-navoption drop-down-parent">
                <span>
                    productos
                </span>
                <DropDown drop_down_name={"productos"}  drop_down_options={[
                    {
                        name: "registrados",
                        link: "/registered-products"
                    },
                    {
                        name: "trackeados",
                        link: "/tracked-products"
                    },
                    {
                        name: "posicionamiento",
                        link: "/positioning"
                    }
                ]}/>
            </span>
            <span class="meli-navoption drop-down-parent">
                <span>
                    administración
                </span>
                <DropDown drop_down_name={"administración"} drop_down_options={[
                    {
                        name: "usuarios",
                        link: "/system-users"
                    },
                    {
                        name: "eventos",
                        link: "/system-events"
                    },
                    {
                        name: "reportes",
                        link: "/system-reports"
                    }
                ]}/>
            </span>
            <span on:click={logout} class="meli-navoption">
                salir
            </span>
        </div>
    </div>
</nav>


<style>
        
    /*=============================================
    =            Header            =
    =============================================*/

    #meli-mvp-header {
        position: fixed;
        width: 100vw;
        max-width: 100%;
        height: var(--navbar-height);
        display: flex;
        align-items: center;
        padding: 0 var(--spacing-h3);
        background: var(--clear-color);
        top: 0;
        left: 0;
        border-bottom: 1px solid var(--primary-color-midlight);
        box-shadow: 0px 0px 20px 9px rgba(0, 0, 0, 0.1);
        z-index: 2;
    }

    #mmh-navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    #mmh-navbar-logo {
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    #mmh-lg-logo {
        width: 9.4vw;
        margin-right: 0.3rem;
    }

    #mmh-lg-logo img {
        width: 100%;
        /* height: 100%; */
    }

    #meli-mvp-options {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        width: 50%;
    }

    .meli-navoption {
        display: flex;
        align-items: center;
        font-size: var(--font-size-1);
        margin: 0 1ex;
        color: var(--primary-color-midlight);
        cursor: default;
        padding: var(--spacing-1);
        border-radius: var(--boxes-roundness);
        transition: all 0.2s ease-in-out;
    }
    
    .meli-navoption a {
        color: var(--primary-color-midlight);
        text-decoration: none;
        transition: all 0.2s ease-in-out;
    }

    .meli-navoption.drop-down-parent {
        border-radius: var(--boxes-roundness) var(--boxes-roundness) 0 0 !important;
    }

    @media (pointer: fine) {
        .meli-navoption:hover {
            color: var(--clear-color) !important;
            background: var(--primary-color-midlight);
            box-shadow: 0px 0px 13px 3px rgba(0, 0, 0, 0.1) !important;
            transform: scale(1.05);
        }

        .meli-navoption:hover a {
            color: var(--clear-color) !important;
        }
    }



</style>