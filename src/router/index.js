import Vue from 'vue'
import Router from 'vue-router'
import Order from '@/components/Order'
import Order2 from '@/components/Order2'
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
      path: '/order2',
      name: 'order2',
      component: Order2
    },
    {
      path: '/search',
      alias: '/',
      name: 'search',
      component: Search
    }
  ]
})
