<script>
    import Input from "../../components/Input/Input.svelte";
    import FieldData, { verifyFormFields } from "../../libs/FieldData";
    import { LoginRequest } from '../../libs/HttpRequests';
    import { push, link } from "svelte-spa-router";
    import bonhart_storage from "../../libs/bonhart-storage";

    const login_request = new LoginRequest();
    let is_form_ready = false;
    let lock_form = false;


    let form_data = [
        new FieldData("customer_username", /[^\n\s;\'\"\`]{2,60}/, "username", "username"),
        new FieldData("customer_password", /[^\n\s]{8,60}/, "password", "password")
    ]

    // Link FormData to the request_data
        $: login_request.username = form_data[0].getFieldValue();
        $: login_request.password = form_data[1].getFieldValue();
    //

    const verifyRegistrationForm = () => {
        if (lock_form) {
            return;
        }

        let is_valid = verifyFormFields(form_data);
        is_form_ready = is_valid;
        form_data = [...form_data]; // trigger svelte update
    }

    const loginUser = () => {
        if(is_form_ready) {
                login_request.do(response => {
                if (response.status === 200) {
                    response.json().then(data => {
                        if ("token" in data) {
                            bonhart_storage.Token = data.token;
                            window.queueMicrotask(() => {
                                push("/");
                            });
                        }
                    })
                } else {
                    console.log(`Error: ${response.status}`);
                    alert("Server error, sorry for the inconvenience");
                }
            })
        }
    }

</script>



<main id="shopsi-login-page">
    <div id="slp-login-wrapper" class="round-box">
        <div id="shopsi-login-title-wrapper">
            <h1>Hey Shopsi</h1>
            <h2>please login</h2>
        </div>
        <div id="slp-login-form-container">
            <form on:submit={() => {}} id="form-fields">
                {#each form_data as field}
                    <div class="form-field-wrapper">
                        <Input
                            field_data={field}
                            isClear={true}
                            isSquared={true}
                            input_label={field.name}
                            onEnterPressed={verifyRegistrationForm}
                            onBlur={verifyRegistrationForm}
                        />
                    </div>
                {/each}
                <button class="full-btn" type="button" on:click={loginUser}>Entrar</button>
            </form>
        </div>
    </div>
</main>

<style>

    #shopsi-login-page {
        --slp-height: calc(100vh - var(--navbar-height));

        display: flex;
        min-height: var(--slp-height);
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: var(--primary-gradient);
        padding: var(--spacing-4) 0;
        z-index: 1;
    }

    :global(#content-wrap:has(#shopsi-login-page)) {
        margin: 0;
    }

    #slp-login-wrapper {
        --login-form-width: 40%;
        --login-form-height: calc(var(--slp-height) * .6);

        color: var(--secondary-color-midlight);
        width: var(--login-form-width);
        min-height: var(--login-form-height);
        background: var(--clear-color);
        padding: var(--spacing-2) var(--spacing-4);
        border: 1px solid #ccc;
    }

    #shopsi-login-title-wrapper {
        text-align: center;
    }

    #shopsi-login-title-wrapper h1 {
        font-size: var(--font-size-h2);
        height: var(--font-size-h1);
        text-transform: capitalize;
        margin: var(--spacing-1) auto;
        padding: 0 var(--spacing-3);
        border-bottom: 2px solid var(--primary-color-midlight);
        width: max-content;
    }

    #shopsi-login-title-wrapper h2 {
        font-size: var(--font-size-2);

        margin: var(--spacing-1) 0;
    }

    #slp-login-form-container {
        margin: var(--spacing-3) 0;
    }

    #form-fields {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    #form-fields .form-field-wrapper {
        margin: var(--spacing-1) 0;
        width: 100%;
    }

    #form-fields > button {
        margin: var(--spacing-3) auto;
    }


</style>