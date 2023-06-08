<script>
    import { newNotification } from "../../../components/notifications/events";
    import { onMount, onDestroy } from "svelte";
    import { GetAllUsersRequest } from "../../../libs/HttpRequests";
    import { users_events } from '../events';
    import UserRow from "./UserRow.svelte";
    import bonhart_storage from '../../../libs/bonhart-storage';

    let users = [];
    
    onMount(() => {
        getAllUsers();

        document.addEventListener(users_events.USERS_LIST_CHANGED, () => {
            getAllUsers();
        });
    })

    onDestroy(() => {
        document.removeEventListener(users_events.USERS_LIST_CHANGED, () => {
            getAllUsers();
        });
    })



    const getAllUsers = () => {
        const request = new GetAllUsersRequest(bonhart_storage.Token);
        
        const on_success = data => {
            users = data;
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
        }

        request.do(on_success, on_error);
    }
</script>

<div id="sup-users-table">
    {#each users as user}
        <UserRow user={user} />
    {/each}
</div>