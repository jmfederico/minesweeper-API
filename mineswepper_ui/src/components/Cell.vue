<template>
  <td :class="'is-' + value">
    <!-- If uncovered, print the number of adjacent bombs. -->
    <div v-if="parseInt(value) === value">
      <!-- Show empty string instead of 0 -->
      {{ value || "" }}
    </div>

    <!-- Is this a bomb?. -->
    <div v-else-if="value === '*'">💣</div>

    <!-- If covered, allow uncovering, and flag toggle. -->
    <template v-else>
      <div @click="$emit('toggleFlag')" class="toggle-flag-action action">
        {{ value === "f" ? "🚩" : "🏳" }}
      </div>
      <div
        v-if="value !== 'f'"
        @click="$emit('uncover')"
        class="uncover-action action"
      >
        🗹
      </div>
    </template>
  </td>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "Cell",
  props: {
    value: {
      type: String,
      required: true
    }
  }
});
</script>

<style lang="scss" scoped>
td {
  margin: 0.1rem;
  width: 3rem;
  height: 4rem;
  background-color: #eee;
  cursor: crosshair;

  .action {
    height: 50%;
  }

  &.is-c {
    background-color: lightgray;
  }

  &.is-\* {
    background-color: lightcoral;
  }

  &.is-f {
    background-color: lightpink;
    .action {
      height: 100%;
    }
  }
}
.is-active td .action {
  cursor: pointer;
}
</style>
