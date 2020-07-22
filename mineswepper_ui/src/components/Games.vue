<template>
  <div>
    <div>
      <label>Which game do you want to play?</label>
      <select v-model="selectedOption">
        <option :value="null">-- Select an option--</option>
        <option v-for="game in games" :key="game.uuid" :value="game.uuid">
          {{ game.uuid }}
        </option>
        <option :value="newGameFlag">A new game</option>
      </select>
    </div>
    <div>
      <Game v-if="selectedGame" :game="selectedGame" />
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
    async loadGames() {
      await this.$axios.get("games/").then(response => {
        this.games = response.data;
      });
    },
    async setNewGame(game) {
      await this.loadGames();
      this.selectedOption = game.uuid;
    }
  }
});
</script>
