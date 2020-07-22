<template>
  <div>
    <table>
      <tr v-for="(_, r) in game.rows" :key="r">
        <td v-for="(_, c) in game.cols" :key="c" :class="'is-' + cell(c, r)">
          <!-- If uncovered, print the number of adjacent bombs. -->
          <div v-if="parseInt(cell(c, r)) === cell(c, r)">{{ cell(c, r) }}</div>

          <!-- Is this a bomb?. -->
          <div v-else-if="cell(c, r) === '*'">💣</div>

          <!-- If covered, allow uncovering, and flag toggle. -->
          <template v-else>
            <div @click="toggleFlag(c, r)" class="toggle-flag-action action">
              {{ cell(c, r) === "f" ? "🚩" : "🏳" }}
            </div>
            <div
              v-if="cell(c, r) !== 'f'"
              @click="uncover(c, r)"
              class="uncover-action action"
            >
              🗹
            </div>
          </template>
        </td>
      </tr>
    </table>
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
  },
  methods: {
    cell(c, r) {
      return this.game.board[c][r];
    },
    uncover(c, r) {
      this.$emit("cellStatus", [c, r, "U"]);
    },
    toggleFlag(c, r) {
      if (this.cell(c, r) !== "f") {
        this.$emit("cellStatus", [c, r, "F"]);
        return;
      }
      this.$emit("cellStatus", [c, r, null]);
    }
  }
});
</script>

<style lang="scss" scoped>
table {
  margin: auto;
}
td {
  margin: 0.1rem;
  width: 3rem;
  height: 4rem;
  background-color: #eee;
  cursor: crosshair;

  .action {
    cursor: pointer;
    height: 50%;
  }

  &.is-c {
    cursor: pointer;
    background-color: lightgray;
  }

  &.is-\* {
    background-color: lightcoral;
  }

  &.is-f {
    background-color: lightseagreen;
    .action {
      height: 100%;
    }
  }
}
</style>
