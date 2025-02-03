<template>
    <div class="message-body">
        <p>That's it for the experiment! Click Finish to go to the end survey, which consists of three surveys, two tests, and some general questions about demographics.</p>
        <a class="button" href="https://tamu.qualtrics.com/jfe/form/SV_eVzNXhPxJ2CnkdT" target="_blank" v-on:click="finishExperiment">Finish</a>
    </div>
</template>

<script>
    export default {
        name: 'stage2-modal',
        methods: {
            finishExperiment() {
                this.$store.dispatch('finishExperiment');
                this.$emit('close-modal');
            }
        }
    }
</script>

<style scoped>

</style>