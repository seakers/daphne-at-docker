<template>
    <div id="question-list">
        <div class="is-title">
            What questions can you ask? What commands can you give?
        </div>
        <div class="is-content">
            These are all the questions or commands that Daphne-AT is able to answer. <br>
            Feel free to rephrase them when querying Daphne! <br><br>
            <ul style="list-style-type: disc; margin-left: 30px">
                <li v-for="questionInfo in questionList">
                    {{questionInfo['question']}} <br>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "QuestionListWindow",

        computed: {
            ...mapGetters({
                questionList: 'getQuestionList'
            }),
        },
    }
</script>

<style scoped>

</style>