<template>
  <div>
    <form @submit="createGame">
      <div>
        <label>
          How many columns:
          <input v-model="cols" type="number" min="3" max="100" />
        </label>
      </div>
      <div>
        <label>
          How many rows:
          <input v-model="rows" type="number" min="3" max="100" />
        </label>
      </div>
      <div>
        <label>
          How many bombs:
          <input v-model="bombs" type="number" min="1" :max="maxBombs" />
        </label>
      </div>
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "NewGameForm",
  data() {
    return {
      cols: 10,
      rows: 10,
      bombs: 15
    };
  },
  computed: {
    newGamePayload() {
      return {
        cols: this.cols,
        rows: this.rows,
        bombs: this.bombs
      };
    },
    maxBombs() {
      const size = (this.cols || 0) * (this.rows || 0);
      return size ? size - 1 : 0;
    }
  },
  methods: {
    async createGame(event) {
      event.preventDefault();
      await this.$axios.post("/games/", this.newGamePayload).then(response => {
        this.$emit("newGame", response.data);
      });
    }
  }
});
</script>
