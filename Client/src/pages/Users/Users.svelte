<script>

    import FieldData, { verifyFormFields } from "../../libs/FieldData";
    import { CreateUserRequest } from "../../libs/HttpRequests";
    import Input from "../../components/Input/Input.svelte";
    import { newNotification } from "../../components/notifications/events";
    import bonhart_storage from "../../libs/bonhart-storage";
    import { emitUsersListChanged } from "./events";
    import UsersTable from "./page-components/UsersTable.svelte";
    import UserEditModal from "./page-components/UserEditModal.svelte";

    const create_user_request = new CreateUserRequest(bonhart_storage.Token);
    let is_form_ready = false;

    let form_data = [
        new FieldData("username", /[a-zA-Z_\-0-9]+/, "Usuario"),
        new FieldData("email", /[a-zA-Z_\-0-9]+@[a-zA-Z_\-0-9]+\.[a-zA-Z_\-0-9]+/, "Correo"),
        new FieldData("password", /[a-zA-Z_\-0-9]+/, "Contraseña", "password")
    ];

    // Link the form data to the request
        $: create_user_request.username = form_data[0].getFieldValue();
        $: create_user_request.email = form_data[1].getFieldValue();
        $: create_user_request.password = form_data[2].getFieldValue();
    //

    const verifyLoginForm = () => {
        let is_valid = verifyFormFields(form_data);
        is_form_ready = is_valid;
        form_data = [...form_data];
    }

    const resetForm = form_fields => {
        form_fields.forEach(field => {
            field.clear();
        })
    }

    const createUser = () => {
        if (!is_form_ready) {
            newNotification(`No se puede crear el usuario, hay campos inválidos`);
            return;
        }

        const on_success = () => {
            newNotification(`Usuario creado con éxito`);
            resetForm(form_data);
            emitUsersListChanged();
        }

        const on_error = status_code => {
            switch(status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                case 409:
                    newNotification(`El usuario o correo ya existe`);
                    break;
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
                    break;
            }   
            resetForm(form_data);
        }

        create_user_request.do(on_success, on_error);
    }
</script>

<UserEditModal />
<main id="system-users-page">
    <div id="sup-content-wrapper">
        <header>
            <h1 class="page-title">Usuarios del sistema</h1>
        </header>
        <div id="sup-new-user-form">
            <h3 class="sup-subtitle" id="sup-nuf-title">
                Nuevo usuario
            </h3>
            <form>
                {#each form_data as field}
                    <div class="form-item-wrapper form-input">
                        <Input 
                            field_data={field}
                            input_label={field.name}
                            input_color="var(--clear-theme-color)"
                            input_dark_color="var(--clear-color)"
                            input_padding="var(--spacing-1) var(--spacing-1)"
                            font_size="var(--font-size-small)"
                            onEnterPressed={verifyLoginForm}
                            onBlur={verifyLoginForm}
                        />
                    </div>
                {/each}
                <div class="form-item-wrapper form-creat-btn">
                    <button on:click={createUser} class="clear-btn">Crear</button>
                </div>
            </form>
        </div>
        <div id="sup-users-table">
            <h3 class="sup-subtitle"  id="sup-users-title">
                usuarios
            </h3>
            <div id="sup-ut-usert-container">
                <UsersTable />
            </div>
        </div>
    </div>
</main>

<style>
    #system-users-page {
        margin-top: var(--navbar-height);
        min-height: calc(100vh - var(--navbar-height));
        background: var(--primary-gradient);
        display: grid;
        place-items: center;
    }
    
    #sup-content-wrapper {
        width:50%;
        background: white;
        min-height: inherit;
        box-shadow: var(--boxes-shadow-2);
    }
    
    header h1{
        color: var(--dark-light-color);
        margin-left: var(--spacing-2);
    }

    .sup-subtitle {
        color: var(--secondary-color);
        padding: 0 0  var(--spacing-2) var(--spacing-2);
        border-bottom: 1px solid var(--secondary-color);
    }

    #sup-new-user-form {
        margin-top: var(--spacing-h4);
    }

    #sup-new-user-form form {
        display: grid;
        box-sizing: content-box;
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-2);
        background: var(--tertiary-color);
        align-items: center;
        padding: var(--spacing-3) var(--spacing-2);
        box-shadow: var(--boxes-shadow);
    }

    .form-item-wrapper.form-creat-btn {
        justify-self: center;
    }

    #sup-users-table {
        margin-top: var(--spacing-3);
    }

    #sup-users-title {
        font-weight: 500;
    }
</style>