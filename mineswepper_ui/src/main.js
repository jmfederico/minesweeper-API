import Vue from "vue";
import App from "./App.vue";
import axios from "axios";

Vue.config.productionTip = false;

Vue.prototype.$axios = axios.create({
  baseURL: process.env.VUE_APP_API_DOMAIN
});

new Vue({
  render: h => h(App)
}).$mount("#app");
