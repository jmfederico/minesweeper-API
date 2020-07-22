import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import vueCookies from "vue-cookies";

Vue.config.productionTip = false;

Vue.prototype.$axios = axios.create({
  baseURL: process.env.VUE_APP_API_DOMAIN
});
Vue.use(vueCookies);

new Vue({
  render: h => h(App)
}).$mount("#app");
