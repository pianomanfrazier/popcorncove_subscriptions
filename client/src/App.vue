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
              <router-link to="/">
              Place or Edit a Subscription
              </router-link>
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile class="menu-tile">
          <v-list-tile-action>
            <v-icon>fas fa-plus-circle</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              <router-link to="/items">
                Add Subscription Item
              </router-link>
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
      <v-tooltip bottom max-width="250px">
        <v-btn slot="activator" @click="exportDialog = true" style="margin-left: auto; margin-right: auto; display: block;">
          <v-icon>fas fa-download</v-icon>
          &nbsp; Export Monthly Report
        </v-btn>
        <span>Download this month's subscription report for all customers in the database.</span>
      </v-tooltip>
    </v-navigation-drawer>


    <v-dialog v-model="exportDialog" width="600px">
      <v-card tile>
        <v-card-title>
          <h2>Choose a Subscription Month</h2>
        </v-card-title>
        <v-card-actions>
        </v-card-actions>
        <v-layout row wrap>
          <v-flex text-xs-center>
            <v-date-picker v-model="subscriptionMonth" type="month"></v-date-picker>
          </v-flex>
        </v-layout>
        <v-card-actions>
          <v-btn @click="exportDialog = false">Close</v-btn>
          <v-btn :href="exportLink()" :disabled="!subscriptionMonth" class="success">Get Subscription</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
  name: 'App',
  data () {
    return {
      exportDialog: false,
      subscriptionMonth: ''
    }
  },
  mounted () {
    // set default export month to next month
    let now = new Date();
    let current = new Date();
    if (now.getMonth() == 11) {
      current = new Date(now.getFullYear() + 1, 0, 1);
    } else {
      current = new Date(now.getFullYear(), now.getMonth() + 1, 1);
    }
    let month = current.getMonth() + 1 < 10 ? `0${current.getMonth() + 1}` : `${current.getMonth() + 1}`
    this.subscriptionMonth = `${current.getFullYear()}-${month}`
  },
  methods: {
    exportLink () {
      let date = this.subscriptionMonth.split('-')
      return `/api/v1/export?year=${date[0]}&month=${date[1]}`
    }
  }
}
</script>

<style>
#app {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}
</style>
