<template>
  <div class="message-body">
    <div v-if="!isSecondUser">
      <p>Hello! You need to be registered user to use Daphne. If you are already registered, please add you username and
        password below.</p>
      <form id="login-form">
        <p style="color: red; font-weight: bold" v-if="hasLoginError">{{ loginError }}</p>
        <div class="field">
          <label class="label">Username</label>
          <div class="control has-icons-left">
            <input class="input" type="text" placeholder="Your username" name="username">
            <span class="icon is-small is-left"><i class="fas fa-user"></i></span>
          </div>
        </div>

        <div class="field">
          <label class="label">Password</label>
          <div class="control has-icons-left">
            <input class="input" type="password" placeholder="Password" name="password">
            <span class="icon is-small is-left"><i class="fas fa-key"></i></span>
          </div>
        </div>

        <div class="field">
          <button class="button" style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                  id="send_command" v-on:click.prevent="login">Submit
          </button>
        </div>
      </form>

      <p>If you do not have a username, you can either register by clicking <a
          v-on:click.prevent="openRegisterForm">here</a> or <a v-on:click.prevent="$emit('close-modal')">continue as a
        guest</a>.</p>
      <p>In case you have forgotten your password, click <a v-on:click.prevent="openResetPasswordForm">here</a> to
        recover
        it.</p>
    </div>
    <div v-if="isSecondUser" style="justify-content: center">
      <p v-if="isSecondUser">{{ loginAlert }}</p>
      <div style="display: flex; justify-content: center;">
      <button class="button" style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E" v-on:click.prevent="loginAfterPopup">Yes
      </button>
      <button class="button" style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E" v-on:click.prevent="continueAsGuest">No
      </button>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
import {wsTools} from "../scripts/websocket-tools";

export default {
  name: 'login-modal',
  computed: {
    ...mapState({
      isLoggedIn: state => state.auth.isLoggedIn,
      hasLoginError: state => state.auth.hasLoginError,
      isSecondUser: state => state.auth.isSecondUser,
      loginAlert: state => state.auth.loginAlert,
      loginError: state => state.auth.loginError,
      username: state => state.auth.username,
      password: state => state.auth.password,
    }),
    ...mapGetters({
      telemetryIsOngoing: 'getTelemetryIsOngoing',
    }),
  },
  methods: {
    login() {
      let formData = new FormData(document.getElementById('login-form'));
      this.$store.dispatch('loginUser', {
        username: formData.get("username"),
        password: formData.get("password"),
        daphneVersion: 'AT',
        isSecondUser: this.isSecondUser
      }).then(async () => {
        // Start the Websocket
        console.log('Submit LOGIN');
      });
      let sECLSSUsers = ["kyleyork2023"];
      if (sECLSSUsers.includes(formData.get("username"))) {
        this.$store.commit('mutateHeraUser', false);
      } else {
        this.$store.commit('mutateHeraUser', true);
      }

      this.$store.commit('addDialoguePiece', {
        "voice_message": `Hi ${this.username}`,
        "visual_message_type": ["text"],
        "visual_message": ['Hi ' + this.username + ', how can I help?'], // Mapping each item to its detection_text property
        "writer": "daphne"
      });
    },
    loginAfterPopup() {
        this.$store.dispatch('loginUser', {
        username: this.username,
        password: this.password,
        daphneVersion: 'AT',
        isSecondUser: this.isSecondUser
      }).then(async () => {
        // Start the Websocket
        console.log('Submit LOGIN');
      });
      let sECLSSUsers = ["kyleyork2023"];
      if (sECLSSUsers.includes(this.username)) {
        this.$store.commit('mutateHeraUser', false);
      } else {
        this.$store.commit('mutateHeraUser', true);
      }
    },
    openRegisterForm() {
      this.$store.commit('activateModal', 'RegisterModal');
    },
    openResetPasswordForm() {
      this.$store.commit('activateModal', 'ResetPasswordModal');
    },
    continueAsGuest() {
      this.$store.commit('mutateUsername', 'guest');
      this.$emit('close-modal');
    }
  },
  watch: {
    isLoggedIn: function (val, oldVal) {
      if (this.isLoggedIn) {
        this.$emit('close-modal');
      }
    }
  }
}
</script>

<style scoped>

</style>
