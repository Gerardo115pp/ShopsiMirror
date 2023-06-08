<script>
    import { newNotification } from "../../../components/notifications/events";
    import FieldData, { verifyFormFields} from "../../../libs/FieldData";
    import Input from "../../../components/Input/Input.svelte";
    import { PatchUserRequest } from "../../../libs/HttpRequests";
    import { onMount, onDestroy } from "svelte";
    import { users_events, emitUsersListChanged } from "../events";
    import bonhart_storage from "../../../libs/bonhart-storage";

    let show_modal = false;
    
    let user_data={
        id: 0,
        username: "username",
        email: "email",
        password: "password"
    }

    $: user_data.password = "";


    let is_form_ready = false;
    let form_data = [
        new FieldData("edit_username", /[a-zA-Z_\-0-9]+/, "Usuario"),
        new FieldData("edit_email", /[a-zA-Z_\-0-9]+@[a-zA-Z_\-0-9]+\.[a-zA-Z_\-0-9]+/, "Correo"),
        new FieldData("edit_password", /[a-zA-Z_\-0-9]+/, "Contraseña", "password", false)
    ];

    onMount(() => {
        document.addEventListener(users_events.START_USER_EDIT, showModal)
    });

    onDestroy(() => {
        document.removeEventListener(users_events.START_USER_EDIT, showModal)
    });

    const resetFormValues = () => {
        form_data[0].setFieldValue(user_data.username);
        form_data[1].setFieldValue(user_data.email);
        form_data[2].setFieldValue("");
    }

    const showModal = event => {
        const { detail:new_user_data } = event;
        user_data = new_user_data;
        show_modal = true;
        window.queueMicrotask(resetFormValues);
    }

    const verifyUserEditRequest = () => {
        let is_valid = verifyFormFields(form_data);
        is_form_ready = is_valid;
        form_data = [...form_data];
    }

    const editUser = () => {
        if (!is_form_ready) {
            newNotification(`No se puede editar el usuario, hay campos inválidos`);
            return;
        }

        const patch_request = new PatchUserRequest(bonhart_storage.Token);
        patch_request.id = user_data.id;
        patch_request.username = form_data[0].getFieldValue();
        patch_request.email = form_data[1].getFieldValue();
        patch_request.password = form_data[2].getFieldValue();

        const on_success = () => {
            newNotification(`Usuario editado con éxito`);
            emitUsersListChanged();
            show_modal = false;
        }

        const on_error = () => {
            newNotification(`No se pudo editar el usuario`);
        }

        patch_request.do(on_success, on_error);
    }


</script>

{#if show_modal}
     <div id="sup-user-edit-modal-wrapper">
         <div id="sup-ud-modal">
            <div id="sup-udm-header">
                <h3>
                    Editar usuario
                </h3>
                <div on:click={() => show_modal = false}  id="sup-udm-close-btn">
                    <span class="material-symbols-outlined">
                        close
                    </span>
                </div>
            </div>
            {#each form_data as field}
                <div class="sup-udm-input-wrappper">
                    <Input 
                        field_data={field}
                        input_label={field.name}
                        input_color="var(--clear-theme-color)"
                        input_dark_color="var(--clear-color)"
                        input_padding="var(--spacing-1) var(--spacing-1)"
                        font_size="var(--font-size-small)"
                        onKeypressed={verifyUserEditRequest}
                        onBlur={verifyUserEditRequest}
                    />
                </div>
            {/each}
            <button on:click={editUser}  class="clear-btn" id="sup-udm-edit-btn">Confirmar</button>
         </div>
     </div>
{/if}

<style>
    /* DEBUG */
    /* * {
        border: 1px solid red;
    } */

    #sup-user-edit-modal-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--dark-tranparent-background);
        display: grid;
        place-items: center;
    }

    #sup-ud-modal {
        display: flex;
        width: 50%;
        gap: var(--spacing-2);
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        background: var(--primary-gradient);
        box-shadow: var(--boxes-shadow);
        padding: var(--spacing-1);
        border-radius: var(--boxes-roundness);
    }

    #sup-udm-header {
        display: grid;
        width: 100%;
        text-align: center;
        grid-template-columns: auto 5ch;
        font-weight: 300;
        color: var(--tertiary-color-light);
        align-items: center;
    }

    #sup-udm-close-btn {
        display: grid;
        place-items: center;
        cursor: pointer;
    }

    .sup-udm-input-wrappper {
        width: 80%;
    }

</style>