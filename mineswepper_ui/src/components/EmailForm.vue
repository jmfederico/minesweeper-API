<template>
  <div>
    <form @submit="setEmail">
      <label>
        your email:
        <input
          v-model="email"
          type="email"
          pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
          title="Email must contain a full domain. user@example.com"
        />
      </label>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "EmailForm",
  data() {
    return {
      email: ""
    };
  },
  methods: {
    setEmail(event) {
      event.preventDefault();
      this.$emit("email", this.email);
    }
  }
});
</script>
