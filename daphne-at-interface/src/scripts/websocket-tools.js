import ReconnectingWebSocket from "reconnecting-websocket";

class WebsocketTools {
    constructor() {
        this.websocket = null;
    }

    async wsConnect(store) {
        return new Promise((resolve, reject) => {
            // Websocket connection
            let websocket = new ReconnectingWebSocket(WS_URL + 'at/ws');
            let pingIntervalId = null;

            websocket.onopen = () => {
                // Start ping routine
                pingIntervalId = setInterval(() => {
                    console.log("Ping sent to the backend!");
                    websocket.send(JSON.stringify({"type": "ping"}));
                }, 10000);

                // Resolve the promise
                this.websocket = websocket;
                resolve();
            };
            websocket.onclose = (event) => {
                console.log("Websockets closed", event);
                clearInterval(pingIntervalId);
            };
            websocket.onmessage = (event) => store.dispatch("onWebsocketsMessage", event);
        });
    }

    async experimentWsConnect() {
        return new Promise((resolve, reject) => {
            let experimentWebsocket = new ReconnectingWebSocket(WS_URL + 'at/experiment');
            experimentWebsocket.onopen = () => {
                this.experimentWebsocket = experimentWebsocket;
                resolve();
            };
            experimentWebsocket.onmessage = function (data) {};
        });

    }

    async wsRefresh() {
        try {
            this.websocket.refresh();
        }
        catch(err) {
            console.log(err);
        }
    }

    async experimentWsRefresh() {
        this.experimentWebsocket.refresh();
    }
}

export let wsTools = new WebsocketTools();
