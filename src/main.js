// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import App from './App'
import router from './router'
import axios from 'axios'
import format from 'date-fns/format'

Vue.config.productionTip = false
Vue.use(Vuetify)
Vue.prototype.$http = axios

Vue.filter('formatDate', function (dt) {
  return format(dt, 'MMM YYYY')
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
