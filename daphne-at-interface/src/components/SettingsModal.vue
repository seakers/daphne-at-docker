<template>
  <div id="settings" class="container-settings">
    <div class="header">
      <div class="header-logo">
        Themes
      </div>
      <div class="header-settings">
        <button type="button" class="header--theme-button active" style="--theme-primary:black; --theme-secondary:#0AFEFF;" v-on:click.prevent="themeDark">
        </button>
        <button type="button" class="header--theme-button" style="--theme-primary:white; --theme-secondary:#0AFEFF;" v-on:click.prevent="themeLight">
        </button>
      </div>
    </div>
    <div class="nav">
      <ul class="nav-links">
        <li class="nav-links--link active">
          Detection
        </li>
      </ul>
    </div>

    <div class="content">
      <div class="content-links--link">
        <p>No anomalous symptoms detected.</p>
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
    themeDark() {
      document.documentElement.dataset.theme = 'dark';
    },
    themeLight() {
      document.documentElement.dataset.theme = 'light';
    }
  },
  watch: {
    theme(theme) {
      document.documentElement.dataset.theme = theme;
    },
  }
}
</script>

<style scoped>

</style>