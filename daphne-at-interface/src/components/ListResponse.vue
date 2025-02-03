<template>
    <div>
        <p v-html="response.begin"></p>
        <ul>
            <li v-for="element in response.list" v-html="element"></li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: 'list-response',
        props: ['response'],
    }
</script>

<style scoped>
</style>