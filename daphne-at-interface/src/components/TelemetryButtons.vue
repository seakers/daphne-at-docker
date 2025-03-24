<template>
    <div id="telemetry-feed">
        <div class="is-title">
            Telemetry Buttons
            (This window will never be shown to the user, it's only for development purposes)
        </div>
        <div class="is-centered is-content">
            <a v-if="!this.telemetryIsOngoing"
               class="button is-telemetry-button is-green" v-on:click.prevent="startTelemetry">
                START RECEIVING
            </a>
            <a v-else
               class="button is-telemetry-button is-red" v-on:click.prevent="stopFakeTelemetry">
                STOP RECEIVING
            </a>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapMutations } from 'vuex';
    import {wsTools} from "../scripts/websocket-tools";

    export default {
        name: "TelemetryButtons",

        computed: {
            ...mapGetters({
                telemetryIsOngoing: 'getTelemetryIsOngoing',
            }),
        },

        methods: {
            startTelemetry() {
                // Start fake telemetry
                console.log('Trying to start fake telemetry...');
                wsTools.websocket.send(JSON.stringify({
                    'type': 'start_fake_telemetry',
                    'attempt': '1'
                }));
            },
            stopFakeTelemetry() {
                wsTools.websocket.send(JSON.stringify({
                    'type': 'stop_telemetry',
                    'attempt': '1'
                }));
            },
        },
    }
</script>

<style scoped>

</style>