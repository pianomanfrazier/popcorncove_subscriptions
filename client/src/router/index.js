import Vue from 'vue'
import Router from 'vue-router'
import Order from '@/components/Order'
import Items from '@/components/Items'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'order',
      component: Order
    },
    {
      path: '/items',
      name: 'items',
      component: Items
    }
  ]
})
