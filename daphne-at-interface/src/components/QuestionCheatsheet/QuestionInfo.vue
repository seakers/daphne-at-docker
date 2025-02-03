<template>
    <div id="question-list">
        <div class="is-title">
            What is the answer for each question? What information should you provide?
        </div>
        <div class="is-content">
            Select questions from the dropdown menu to see more information about them. <br><br>
        </div>
        <div class="is-content is-multiselect">
            <multiselect
                    :value="value"
                    :options="options"
                    :multiple="true"
                    :searchable="true"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :preserve-search="true"
                    :allow-empty="true"
                    placeholder="Search and/or select the questions you want information about."
                    label="name"
                    selectLabel="Click to select"
                    deselectLabel="Click to remove"
                    openDirection="below"
                    track-by="name"
                    :preselect-first="false"
                    @select="newSelection"
                    @remove="newDeselection">
            </multiselect>
        </div>
        <div v-for="(questionInfo, questionName) in questionDict" class="is-content">
            <div class="horizontal-divider" style="margin-bottom: 10px"></div>
            <u>Question/Command:</u> {{questionName}} <br>
            <p style="margin-left: 40px">
                <u>Required parameters:</u> {{questionInfo['parameters']}} <br>
                <u>Provided answer:</u> {{questionInfo['answer']}}
            </p>
            <div class="horizontal-divider" style="margin-top: 10px"></div>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex'
    import Multiselect from 'vue-multiselect'

    export default {
        name: "QuestionInfoWindow",

        computed: {
            ...mapGetters({
                questionList: 'getQuestionList',
                selectedQuestionsList: 'getSelectedQuestionsList'
            }),
            value ()  {
                let aux = [];
                for (let index in this.selectedQuestionsList) {aux.push({'name': this.selectedQuestionsList[index]})}
                return aux;
            },
            options ()  {
                let aux = [];
                for (let i = 0; i < this.questionList.length; i++) {aux.push({'name': this.questionList[i]['question']})}
                return aux;
            },
            questionDict () {
                let aux = {};
                for (let i = 0; i < this.questionList.length; i++) {
                    let questionInfo = this.questionList[i];
                    let question = questionInfo['question'];
                    if (this.selectedQuestionsList.includes(question)) {
                        aux[question] = {'parameters': questionInfo['parameters'], 'answer': questionInfo['answer']};
                    }
                }
                return aux;
            }
        },

        methods: {
            async newSelection(selectedQuestion) {
                let question = selectedQuestion['name'];
                if (!this.selectedQuestionsList.includes(question)) {await this.$store.dispatch('addSelectedQuestion', question)}
            },
            async newDeselection(deselectedQuestion) {
                let question = deselectedQuestion['name'];
                await this.$store.dispatch('removeSelectedQuestion', question)
            },
        },

        components: {
            Multiselect,
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>

</style>