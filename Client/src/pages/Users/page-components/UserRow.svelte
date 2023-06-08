<script>

    import { DeleteUserRequest, GetMeliOauthUrlRequest } from '../../../libs/HttpRequests';
    import { emitUsersListChanged, emitStartUserEdit } from '../events';
    import { newNotification } from '../../../components/notifications/events';
    import bonhart_storage from '../../../libs/bonhart-storage';
    
    export let user={
        id: "shopsi-user-xxxxxx",
        username: "username",
        email: "email"
    };

    const deleteUser = () => {
        const delete_request = new DeleteUserRequest(bonhart_storage.Token);

        delete_request.username = user.username;
        delete_request.email = user.email;

        const on_success = () => {
            newNotification(`Usuario eliminado con éxito`);
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
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
            }
        };

        delete_request.do(on_success, on_error);
    }

    const editUser = () => {
        emitStartUserEdit(user);
    }

    const linkMeliAccount = () => {
        const oauth_request = new GetMeliOauthUrlRequest(bonhart_storage.Token);

        const on_success = data => {
            window.location.href = data.url;
            // console.log(data.url);
        }

        const on_error = status_code => {
            switch(status_code) {
                case 500:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo`);
                    break;
                case 400:
                    newNotification("No deberias estar viendo esto, favor de reportarlo: 400");
                    break;
                default:
                    newNotification(`Se encontro un error inesperado, favor de reportarlo: ${status_code}`);
            }
        };

        oauth_request.do(on_success, on_error);
    }
</script>

<div class="sup-user-row">
    <div class="sup-user-row-username sup-user-info">
        {user.username}
    </div>
    <div class="sup-user-row-email sup-user-info">
        {user.email}
    </div>
    <div class="sup-user-controls">
        <button on:click={editUser} class="full-two-btn sup-controls-action" id="sup-ca-edit">
            <span class="material-symbols-outlined">
                key
            </span>
        </button>
        <button on:click={deleteUser} class="full-two-btn sup-controls-action" id="sup-ca-delete">
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <button on:click={linkMeliAccount} class="full-two-btn sup-controls-action" id="sup-ca-delete">
            <span class="material-symbols-outlined">
                add_link
            </span>
        </button>
    </div>
</div>

<style>
    /* DEBUG */
    /* * {
        border: 1px solid red;
    } */

    .sup-user-row {
        display: grid;
        box-sizing: content-box;
        grid-template-columns: 1fr 1fr minmax(30ch, 40%);
        background-color: var(--secondary-color-dark);
        color: var(--clear-color);
        padding: var(--spacing-2);
    }

    .sup-user-row:not(:last-child) {
        border-bottom: 1px solid var(--tertiary-color-light);
    }

    .sup-user-info {
        display: grid;
        align-content: center;
    }

    .sup-user-controls {
        display: flex;
        gap: 1em;
        justify-content: center;
    }

</style>