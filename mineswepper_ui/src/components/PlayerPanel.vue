<template>
  <div>
    <div>
      <h1>Welcome to Deviget MineSweeper Plus ++ Mega Ultimate</h1>
    </div>
    <div v-if="!email">
      <EmailForm @email="email = $event" />
    </div>
    <div v-else>
      <div>Welcome {{ email }} - <a href="" @click="logout">Log out</a></div>
      <Games :email="email" />
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import EmailForm from "./EmailForm.vue";
import Games from "./Games.vue";

export default Vue.extend({
  name: "PlayerPanel",
  data() {
    return {
      email: null
    };
  },
  components: {
    EmailForm,
    Games
  },
  created() {
    // Keep last user session!
    const email = this.$cookies.get("email");
    if (email) {
      this.email = email;
    }
  },
  methods: {
    logout(event) {
      event.preventDefault();
      this.email = null;
    }
  },
  watch: {
    email(newEmail) {
      this.$axios.defaults.auth = null;
      this.$cookies.remove("email");
      if (newEmail) {
        // Keep session across reloads!
        this.$cookies.set("email", newEmail, 0);
        this.$axios.defaults.auth = {
          username: this.email,
          password: this.email
        };
      }
    }
  }
});
</script>
