<template>
    <p v-html="response"></p>
</template>

<script>
    export default {
        name: 'text-response',
        props: ['response'],
    }
</script>

<style scoped>
</style>