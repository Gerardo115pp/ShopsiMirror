export const rapid_report_messages = {
    STAGE_CHANGED: 'stage_changed',
    PROGRESS_MADE: 'progress_made',
    REPORT_FINISHED: 'report_finished',
    ERROR_OCCURRED: 'error_occurred',
    REPORT_STARTED: 'report_started',
    REPORT_UNSTARTED: 'report_unstarted'
}
const ws_product_server = WS_PRODUCT_SERVER;

export default class RapidReportTransmisor {
    constructor() {
        this.status = 0;
        this.host = `${ws_product_server}/reports/rapid-report`;
        this.is_connected = false;
        this.report_length = 0;
        this.report_progress = 0;
        this.socket = undefined;
        this.disconnection_callback = () => {};
        this.connection_callback = () => {};
        this.message_callback = () => {};
    }

    get isConnected () {
        return this.is_connected === 1 ? true : false;
    }

    connect = () => {
        this.socket = new WebSocket(this.host);
        this.socket.onopen = this.onOpen;
        this.socket.onclose = this.onClose;
        this.socket.onmessage = this.onMessage;
        this.socket.onerror = this.onError;
    }

    set onConnection (callback) {
        this.connection_callback = callback;
    }

    set onDisconnection (callback) {
        this.disconnection_callback = callback;
    }

    onOpen = (event) => {
        this.is_connected = 1;
        if (this.connection_callback !== undefined) {
            this.connection_callback();
        }
    }

    onClose = (event) => {
        this.is_connected = 0;
        console.log('Connection closed');
        if (this.disconnection_callback !== undefined) {
            this.disconnection_callback();
        }
    }

    Close = () => {
        this.socket.close();
    }


    onMessage = (event) => {
        const data = JSON.parse(event.data);
        this.message_callback(data);
    }

    onError = (event) => {
        console.log(event);
    }

    emit = (event, data) => {
        this.socket.send(JSON.stringify({
            event: event,
            data: data
        }));
    }





}