import Vue from 'vue'
import Router from 'vue-router'
import Order from '@/components/Order'
import Search from '@/components/Search'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/order',
      name: 'order',
      component: Order
    },
    {
      path: '/search',
      alias: '/',
      name: 'search',
      component: Search
    }
  ]
})
