<template>
  <div>
    <div>
      <h1>Welcome to our MineSweeper Plus ++ 2025</h1>
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
  }
});
</script>
