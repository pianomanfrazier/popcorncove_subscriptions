<template>
  <div id="app">
    <v-app>
    <!-- side bar menu -->
    <v-navigation-drawer app fixed value="true" stateless permanent>
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
        <v-list-tile class="menu-tile">
          <v-list-tile-action>
            <v-icon>fas fa-shopping-cart</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              Place or Edit a Subscription
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
      <v-tooltip bottom max-width="250px">
        <v-btn slot="activator" style="margin-left: auto; margin-right: auto; display: block;">
          <v-icon>fas fa-download</v-icon>
          &nbsp; Export Monthly Report
        </v-btn>
        <span>Download this month's subscription report for all customers in the database.</span>
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
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}
</style>
