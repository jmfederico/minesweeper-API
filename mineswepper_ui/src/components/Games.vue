<template>
  <div>
    <div>
      <label>
        Which game do you want to play?
        <select v-model="selectedOption">
          <option :value="null">-- Select an option--</option>
          <option v-for="game in games" :key="game.uuid" :value="game.uuid">
            {{ getStatusIcon(game) }} {{ game.cols }} x {{ game.rows }} -
            {{ game.uuid }}
          </option>
          <option :value="newGameFlag">A new game</option>
        </select>
      </label>
    </div>
    <div>
      <Game
        v-if="selectedGame"
        :game="selectedGame"
        @cellStatus="handleCellStatus"
      />
      <NewGameForm v-if="selectedOption == newGameFlag" @newGame="setNewGame" />
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import Game from "./Game.vue";
import NewGameForm from "./NewGameForm.vue";

export default Vue.extend({
  name: "Games",
  components: {
    Game,
    NewGameForm
  },
  props: {
    email: {
      type: String,
      required: true
    }
  },
  data() {
    const newGameFlag = "__new__";
    return {
      newGameFlag,
      games: [],
      selectedOption: null
    };
  },
  created() {
    this.loadGames();
  },
  computed: {
    selectedGame() {
      return this.games.find(game => game.uuid == this.selectedOption);
    }
  },
  methods: {
    getStatusIcon(game) {
      if (game.won) {
        return "✅";
      }

      if (game.finished) {
        return "❌";
      }

      return "▶️";
    },
    async loadGames() {
      await this.$axios
        .get("games/")
        .then(response => {
          this.games = response.data;
        })
        .catch(() => {
          alert("Something failed!");
          alert("And I did not write complete error handlers.");
          alert("So you get this annoying alerts.");
        });
    },
    async setNewGame(game) {
      await this.loadGames();
      this.selectedOption = game.uuid;
    },
    async handleCellStatus([c, r, status]) {
      const url = `games/${this.selectedOption}/cells/${c},${r}/`;
      await this.$axios.patch(url, { status }).catch(() => {
        alert("Something failed!");
        alert("And I did not write complete error handlers.");
        alert("So you get this annoying alerts.");
      });
      this.loadGames();
    }
  }
});
</script>

<style lang="scss" scoped>
select {
  height: 3rem;
}
</style>
