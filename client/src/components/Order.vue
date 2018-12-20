<template>
<div>
  <v-stepper v-model="stepper">
    <v-stepper-header>
      <v-stepper-step :complete="stepper > 1" step="1">
        Choose or create a customer
      </v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="stepper > 2" step="2">
        Create or Change a Subscription
      </v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="stepper > 3" step="3">
        Choose a Shipping Address
      </v-stepper-step>
    </v-stepper-header>
    <v-stepper-items>
      <v-stepper-content step="1">
        <Customer
          @update:customer="customer = $event"
          @next="stepper=2"
        />
      </v-stepper-content>
      <v-stepper-content step="2">
        <Subscription
          :customer="customer"
          @update:subscription="subscription = $event"
          @next="stepper = 3"
          @previous="stepper = 1"
          @cancel="stepper = 1"
        />
      </v-stepper-content>
      <v-stepper-content step="3">
        <Shipping
          :customer="customer"
          @update:address="shippingAddress = $event"
          @previous="stepper = 2"
          @cancel="stepper = 1"
        />
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>

  <!-- <v-dialog v-model="orderDialog" width="300px">
    <v-card tile>
      <v-card-text>
        You are about to place the following order:
        <p v-if="customer">
        <b>Customer:</b> {{ customer.name.first }} {{ customer.name.last }} <br>
        <b>Item:</b> {{ select }} <br>
        <b>Subscription Dates:</b> {{ startdate | formatDate }} to {{ enddate | formatDate }}
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="orderDialog = false; placeOrder" color="primary">Confirm</v-btn>
        <v-btn @click="orderDialog = false">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog> -->
</div>
</template>

<script>
import Customer from './Customer'
import Subscription from './Subscription'
import Shipping from './Shipping'

export default {
  name: 'order',
  components: {
    Customer,
    Subscription,
    Shipping
  },
  data () {
    return {
      customer: {},
      subscription: {},
      shippingAddress: {},
      orderDialog: false,
      stepper: 1,
    }
  },
  mounted () {
  },
  methods: {
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style scoped>
</style>
