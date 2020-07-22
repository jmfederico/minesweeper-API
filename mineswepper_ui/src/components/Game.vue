<template>
  <div>
    {{ game }}
  </div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "Game",
  props: {
    game: {
      type: Object,
      required: true
    }
  }
});
</script>
