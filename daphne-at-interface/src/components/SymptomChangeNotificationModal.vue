<template>
  <div class="message-body">
    <div style="justify-content: center">
      <p style="text-align: center">I have detected a change in the measurements.</p>
      <div style="display: flex; justify-content: center;">
        <button class="button" style="margin-top:20px; width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E" v-on:click.prevent="closeModal">Ok
        </button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "SettingsModal",
  data: function () {
    return {
      theme: "dark"
    }
  },
  computed: {},
  methods: {
    closeModal(state) {
        this.$store.commit('closeModal');
        // this.$store.dispatch('detectAnomalousSymptoms', true);
    },
  },
  watch: {
  }
}
</script>

<style scoped>

</style>
