<template>
    <div id="experiment-timer">
        <p>{{minutes}} : {{seconds}}</p>
    </div>

</template>

<script>
    export default {
        name: 'timer',
        props: ['duration', 'startTime'],
        data() {
            return {
                now: 0,
                timeInterval: {}
            }
        },
        computed: {
            endTime() {
                return this.startTime + 1000*this.duration;
            },
            endTimer() {
                return (Math.floor(this.endTime - this.now) <= 0);
            },
            minutes() {
                let t = this.endTime - this.now;
                let minutes = Math.floor((t/1000/60) % 60);
                return ('0' + minutes).slice(-2);
            },
            seconds() {
                let t = this.endTime - this.now;
                let seconds = Math.floor((t/1000) % 60);
                return ('0' + seconds).slice(-2);
            }
        },
        methods: {
            createTimeInterval() {
                this.timeInterval = window.setInterval(() => {
                    this.now = Date.now();
                    if (this.endTime - this.now <= 0) {
                        window.clearInterval(this.timeInterval);
                        this.$emit('countdown-end');
                    }
                }, 1000);
            },
            timeUp() {
                this.$root.$emit('endExperiment');
            }
        },
        mounted() {
            this.createTimeInterval();
        },
        watch: {
            startTime: function (val, oldVal) {
                this.createTimeInterval();
            },
            now: function(val, oldVal) {
                if (this.endTimer) {
                    this.timeUp();
                }
            }
        }
    }
</script>

<style scoped>
    #experiment-timer {
        position: fixed;
        top: 5px;
        right: 235px;
        background: #002E2E;
        font-size: 18px;
        font-weight: bold;
        color: #0AFEFF;
        border-width: 1px 1px 1px 1px !important;
        border-color: #0AFEFF !important;
        border-style: solid !important;
        border-radius: 5px 5px 5px 5px;
    }
</style>