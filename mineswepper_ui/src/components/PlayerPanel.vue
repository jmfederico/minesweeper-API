<template>
  <div>
    <div>
      <h1>Welcome to Deviget MineSweeper Plus ++ Mega Ultimate</h1>
    </div>
    <div v-if="!email">
      <EmailForm @email="email = $event" />
    </div>
    <div v-else>
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
  watch: {
    email(newEmail) {
      this.$axios.defaults.auth = null;
      if (newEmail) {
        this.$axios.defaults.auth = {
          username: this.email,
          password: this.email
        };
      }
    }
  }
});
</script>
