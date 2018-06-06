import Vue from 'vue'
import Router from 'vue-router'
import Order2 from '@/components/Order2'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'order',
      component: Order2
    }
  ]
})
