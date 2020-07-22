<template>
  <div>{{ games }}</div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "PlayerPanel",
  props: {
    email: {
      type: String,
      required: true
    }
  },
  data() {
    return { games: [] };
  },
  created() {
    this.loadGames();
  },
  methods: {
    async loadGames() {
      await this.$axios
        .get("games/", {
          auth: {
            username: this.email,
            password: this.email
          }
        })
        .then(response => {
          this.games = response.data;
        });
    }
  }
});
</script>
