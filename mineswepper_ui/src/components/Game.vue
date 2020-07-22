<template>
  <div :class="statusClass">
    <div class="game-status">
      {{ status }}
    </div>

    <table>
      <tr v-for="(_, r) in game.rows" :key="r">
        <td v-for="(_, c) in game.cols" :key="c" :class="'is-' + cell(c, r)">
          <!-- If uncovered, print the number of adjacent bombs. -->
          <div v-if="parseInt(cell(c, r)) === cell(c, r)">
            <!-- Show empty string instead of 0 -->
            {{ cell(c, r) || "" }}
          </div>

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

    <dl>
      <dt>Game time</dt>
      <dd>{{ elapsedTime }}</dd>
      <dt>Number of columns</dt>
      <dd>{{ game.cols }}</dd>
      <dt>Number of rows</dt>
      <dd>{{ game.rows }}</dd>
      <dt>Total cells</dt>
      <dd>{{ game.rows * game.cols }}</dd>
      <dt>Number of bombs</dt>
      <dd>{{ game.bombs }}</dd>
      <dt>Number of flags</dt>
      <dd>{{ flags }}</dd>
    </dl>
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
  data() {
    return {
      elapsedTime: null
    };
  },
  computed: {
    statusClass() {
      if (this.game.won) {
        return "is-finished is-won";
      }

      if (this.game.finished) {
        return "is-finished is-lost";
      }

      return "is-active";
    },
    status() {
      if (this.game.won) {
        return "You have won!";
      }

      if (this.game.finished) {
        return "You have lost!";
      }

      return "You are playing!";
    },
    flags() {
      return this.game.board.reduce((count, col) => {
        return (
          count +
          col.reduce((count, cell) => {
            return count + (cell === "f" ? 1 : 0);
          }, 0)
        );
      }, 0);
    },
    startDatetime() {
      return new Date(this.game.created_at);
    }
  },
  created() {
    setInterval(this.updateGameTimer, 1000);
  },
  methods: {
    updateGameTimer() {
      const endDatetime = this.game.finished
        ? new Date(this.game.finished_at)
        : new Date();
      const delta = Math.floor((endDatetime - this.startDatetime) / 1000);
      const minutes = Math.floor(delta / 60);
      const seconds = delta % 60;

      const minutes_str = minutes === 1 ? "minute" : "minutes";
      const seconds_str = seconds === 1 ? "second" : "seconds";

      this.elapsedTime = `${minutes} ${minutes_str} and ${seconds} ${seconds_str}`;
    },
    cell(c, r) {
      return this.game.board[c][r];
    },
    uncover(c, r) {
      if (this.game.finished) {
        return;
      }
      this.$emit("cellStatus", [c, r, "U"]);
    },
    toggleFlag(c, r) {
      if (this.game.finished) {
        return;
      }
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
.game-status {
  color: blue;
  font-size: 2rem;
  padding: 1rem;
  font-weight: bold;
}
.is-won .game-status {
  color: green;
}
.is-lost .game-status {
  color: red;
}

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
    background-color: lightseagreen;
    .action {
      height: 100%;
    }
  }
}
.is-active td .action {
  cursor: pointer;
}

dl {
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
}
dt,
dd {
  box-sizing: border-box;
  text-align: left;
  margin: 0;
  padding: 0.3rem 1rem;
  width: 50%;
}
dt {
  text-align: right;
  font-weight: bold;
}
</style>
