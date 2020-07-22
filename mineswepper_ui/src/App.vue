<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <PlayerPanel />
  </div>
</template>

<script>
import Vue from "vue";
import PlayerPanel from "./components/PlayerPanel.vue";

export default Vue.extend({
  name: "App",
  components: {
    PlayerPanel
  }
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
