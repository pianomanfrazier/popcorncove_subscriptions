<template>
  <div id="app">
    <v-app>
    <!-- side bar menu -->
    <v-navigation-drawer app value="true" stateless permanent absolute>
      <v-toolbar flat>
      <v-list>
        <v-list-tile>
          <v-list-tile-title class="title">
            Popcorn Cove Subscriptions
          </v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
      <v-list>
        <navitem v-for="item in nav" :item="item" :key="item.title"></navitem>
      </v-list>
      <v-tooltip bottom>
        <v-btn slot="activator" style="margin-left: auto; margin-right: auto; display: block;">
          <v-icon>fas fa-download</v-icon>
          &nbsp; Export Monthly Report
        </v-btn>
        <span>Download this month's subscription report.</span>
      </v-tooltip>
    </v-navigation-drawer>

    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>

    </v-app>
  </div>
</template>

<script>
import navitem from './components/subcomponents/navitem'

export default {
  name: 'App',
  components: {
    navitem
  },
  data () {
    return {
      nav: [
        {
          title: 'Place New Order',
          link: '/order',
          icon: 'shopping-cart'
        },
        {
          title: 'Search Database',
          link: '/search',
          icon: 'search'
        }
      ]
    }
  }
}
</script>

<style>
#app {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}
</style>
