<template>
    <div class="is-seclss-background-black is-vertical-filler">
        <div>
            <div class="is-seclss-background-black" style="height: 10px"></div>
            <div class="box is-main" style="margin:10px">
                <div class="is-title" style="border-width: 0px !important">
                    <div style="height: 10px"></div>
                    <div class="columns">
                        <div class="column is-8">
                            Please select whose screen you want to see (only users currently doing an experiment are available):
                        </div>
                        <div class="column is-4">
                            <div class="field has-addons">
                                <div class="control">
                                    <div class="select">
                                        <select name="subject-list" v-model="selectedSubject">
                                            <option v-for="subject in subjectList" :value="{ userId: subject.id, userName: subject.name }" :key="subject.id">{{ subject.name }}</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="control">
                                    <button type="submit" class="button is-primary" v-on:click="addShownSubject">Add</button>
                                </div>
                                <div class="control">
                                    <button type="submit" class="button is-primary" v-on:click="removeShownSubject">Remove</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="height: 10px"></div>
                </div>
            </div>
            <SubjectViewer class="box is-main" style="margin:40px"
                           v-for="subject in shownSubjects"
                           :user-name="subject['userName']"
                           :user-id="subject['userId']"
                           :key="subject['userId']"
                           v-on:remove-shown="onRemoveShown">
            </SubjectViewer>
            <div class="is-seclss-background-black" style="height: 100px"></div>
        </div>
    </div>
</template>

<script>
    import {fetchGet} from "../../scripts/fetch-helpers";
    import SubjectViewer from "./SubjectViewer";

    export default {
        name: "MCCApp",
        components: {SubjectViewer},
        data() {
            return {
                subjectList: [],
                selectedSubject: {},
                shownSubjects: []
            }
        },
        methods: {
            async updateSubjectList() {
                try {
                    let response = await fetchGet(API_URL + 'experiment-at/subject-list');
                    if (response.ok) {
                        let subjectList = await response.json();
                        this.subjectList = subjectList["subjects"];
                    }
                    else {
                        console.error('Error loading current subjects.');
                    }
                }
                catch(e) {
                    console.error('Networking error:', e);
                }
            },
            addShownSubject() {
                let bool = false;
                for (let index in this.shownSubjects) {
                    if (this.shownSubjects[index].userName === this.selectedSubject.userName) {
                        bool = true;
                        break;
                    }
                }
                if (!bool) {
                    this.shownSubjects.push(this.selectedSubject);
                }
            },
            removeShownSubject() {
                let indexToDelete = -1;
                for (let index in this.shownSubjects) {
                    if (this.shownSubjects[index].userName === this.selectedSubject.userName) {
                        indexToDelete = index;
                    }
                }
                if (indexToDelete != -1){
                    this.shownSubjects.splice(indexToDelete, 1);
                }
            },
            onRemoveShown(userId) {
                console.log("one remove shownnnn")
                let indexToDelete = -1;
                for (let index in this.shownSubjects) {
                    if (this.shownSubjects[index].userId === userId) {
                        indexToDelete = index;
                    }
                }
                if (indexToDelete != -1){
                    this.shownSubjects.splice(indexToDelete, 1);
                }
            }
        },
        mounted() {
            this.updateSubjectList();
            setInterval(this.updateSubjectList, 1200);
        }
    }
</script>

<style scoped>

</style>
