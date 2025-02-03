<template>
    <div class="is-seclss-background-black is-vertical-filler">
        <div class="horizontal-divider"></div>
        <div class="box is-main" style="margin-bottom: 5px">
            <question-list-window></question-list-window>
        </div>
        <div class="box is-main" style="margin-bottom: 5px">
            <question-info-window></question-info-window>
        </div>
        <div style="margin-top: 20px">
            <the-footer></the-footer>
        </div>
    </div>
</template>

<script>
    import {fetchGet} from "../../scripts/fetch-helpers";
    import QuestionListWindow from "./QuestionList";
    import QuestionInfoWindow from "./QuestionInfo";
    import TheFooter from "../TheFooter";

    export default {
        name: "QuestionCheatsheetApp",
        components: {
            TheFooter,
            QuestionInfoWindow,
            QuestionListWindow
        },
        methods: {
        },
        mounted() {
        }
    }
</script>

<style scoped>

</style>