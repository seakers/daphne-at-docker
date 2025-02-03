<template>
  <div>
    <div class="message-body" style="display: flex; justify-content: center; text-align: center">
      <div class="modal-survey" id="survey" style="display:block">
        <p>This is a <b><u>without</u></b> Daphne session. Please close the browser window.</p>
      </div>
      <div class="modal-survey" id="done" style="display:none">
        <p>If you have filled out the survey, click on "Done" button below to return to the experiment.</p>
        <button class="button theme-buttons" v-on:click.prevent="submitAnswer">Done</button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "WithoutDaphneSessionModal",
  computed: {
    isDone: false
  },
  methods: {
    submitAnswer() {
      document.getElementById('survey').style.display = 'block';
      document.getElementById('done').style.display = 'none';
      this.$emit('close-modal')
    },
    fillSurvey() {
      document.getElementById('survey').style.display = 'none';
      document.getElementById('done').style.display = 'block';
      window.open("https://tamu.qualtrics.com/jfe/form/SV_8AlVsnyHiGXWgSO");
    }
  },
  watch: {}
}
</script>

<style scoped>
</style>
