export const users_events = {
    USERS_LIST_CHANGED: 'users_list_changed',
    START_USER_EDIT: 'start_user_edit',
}

export const emitUsersListChanged = () => {
    const event = new CustomEvent(users_events.USERS_LIST_CHANGED);
    document.dispatchEvent(event);
}

export const emitStartUserEdit = (user) => {
    const event = new CustomEvent(users_events.START_USER_EDIT, { detail: user });
    document.dispatchEvent(event);
}