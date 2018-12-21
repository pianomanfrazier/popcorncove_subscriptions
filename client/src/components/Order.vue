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
        <v-card style="max-width: 55em; margin: auto;" flat>
          <v-card-title primary-title><h1 class="headline mb-0">Choose or Create a Customer</h1></v-card-title>

          <v-container grid-list-md text-xs-center>
            <v-layout row wrap>
              <v-flex xs12>
                <h2>Choose a Customer</h2>
              </v-flex>
              <v-flex xs8>
                <v-select
                  v-if="byField === 'name'"
                  v-model="customer"
                  :items="customers"
                  item-text="name"
                  label="Customer Name"
                  autocomplete
                  :filter="customernamefilter"
                  clearable
                ></v-select>
                <v-select
                  v-if="byField === 'email'"
                  v-model="customer"
                  :items="customers"
                  item-text="email"
                  label="Customer Email"
                  autocomplete
                  :filter="customeremailfilter"
                  clearable
                ></v-select>
                <v-select
                  v-if="byField === 'phone'"
                  v-model="customer"
                  :items="customers"
                  mask="phone"
                  item-text="phone"
                  label="Customer Phone"
                  autocomplete
                  :filter="customerphonefilter"
                  clearable
                ></v-select>
              </v-flex>
              <v-flex xs4>
                <v-select
                  v-model="byField"
                  :items="byFields"
                  label="Field"
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-divider></v-divider>
              </v-flex>
            </v-layout>
          </v-container>

          <v-form ref="form" v-model="validCustomer">
            <v-container grid-list-md text-xs-center>
              <v-layout row wrap>
                <v-flex xs12>
                  <h2 class="pt-2">Customer Information</h2>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="name"
                    :rules="nameRules"
                    label="Name"
                    required
                    :disabled="disableCustomerForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="E-mail"
                    required
                    :disabled="disableCustomerForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="phone"
                    :rules="phoneRules"
                    label="Phone Number"
                    mask="phone"
                    required
                    :disabled="disableCustomerForm"
                  ></v-text-field>
                </v-flex>
                <v-flex>
                  <v-btn :disabled="!validCustomer" v-if="!customer" @click="createCustomer();" style="float: left;" color="primary">Create Customer</v-btn>
                  <v-btn :disabled="!validCustomer" v-if="customer && !disableCustomerForm" @click="updateCustomer(); disableCustomerForm = !disableCustomerForm;" style="float: left;">Update Customer</v-btn>
                  <v-btn v-if="customer && disableCustomerForm" @click="disableCustomerForm = !disableCustomerForm" style="float: left;">Edit Customer</v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>

          <v-card-actions class="mt-4">
            <v-btn :disabled="!customer" @click.native="stepper = 2">Next</v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>
      <v-stepper-content step="2">
        <!-- <Shipping
          :customer="customer"
          :customers="customers"
          :address="address"
          :addresses="addresses"
          @update:customer="customer = $event"
          @update:customers="customers = $event"
          @update:address="address = $event"
          @update:addresses="addresses = $event"
          @next="stepper = 3"
          @previous="stepper = 1"
        /> -->
      </v-stepper-content>
      <v-stepper-content step="3">
        <Subscription
          :customer="customer"
          @update:subscription="subscription = $event"
          @previous="stepper = 2"
          @cancel="stepper = 1; customer = {};"
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
import Subscription from './Subscription'
import Shipping from './Shipping'

export default {
  name: 'order',
  components: {
    Subscription,
    Shipping
  },
  data () {
    return {
      customer: {},
      customers: [],
      address: '',
      addresses: [],
      subscription: {},
      subscriptions: [],
      orderDialog: false,
      stepper: 1,
      // Customer Data
      byField: 'name',
      byFields: [
        'name',
        'email',
        'phone'
      ],
      validCustomer: false,
      disableCustomerForm: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => !!v && v.length <= 70 || 'Name must be less than 70 characters'
      ],
      email: '',
      emailRules: [
        v => !!v || 'Phone Number is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,4})+$/.test(v) || 'E-mail must be valid'
      ],
      phone: '',
      phoneRules: [
        v => !!v || 'Phone Number is required',
        v => /\(\d+\)| |-|\d+/.test(v) || 'Phone Number must be valid'
      ],
      customernamefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.name)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      customeremailfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.email)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      customerphonefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.phone)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      customeremailfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.phone)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      // Shipping Data
      // Subscription Data
    }
  },
  mounted () {
    this.getAllCustomers()
  },
  methods: {
    // Customer Methods
    getAllCustomers () {
      this.$http.get('/api/v1/customer')
        .then(res => {
          this.customers = res.data
        })
    },
    createCustomer () {
      if (this.$refs.form.validate()) {
        this.$http
          .post('/api/v1/customer', {
            name: this.name,
            phone: this.phone,
            email: this.email
          })
          .then(res => {
            this.$toasted.show('Customer created')
            this.customer = res.data
            this.getAllCustomers()
          })
          .catch(err => {
            this.$toasted.err('Failed to create customer')
            console.log(err)
          })
      }
    },
    updateCustomer () {
      if (this.$refs.form.validate()) {
        this.$http
          .put(`/api/v1/customer/${this.customer.id}`, {
            name: this.name,
            phone: this.phone,
            email: this.email
          })
          .then(res => {
            this.$toasted.show('Customer updated')
            this.customer = res.data
            this.getAllCustomers()
          })
          .catch(err => {
            this.$toasted.err('Failed to update customer')
            console.log(err)
          })
      }
    }
  },
  computed: {
  },
  watch: {
    customer (val) {
      if (val) {
        this.name = val.name
        this.email = val.email
        this.phone = val.phone
        this.disableCustomerForm = true
      } else {
        this.$refs.form.reset()
        this.disableCustomerForm = false
      }
    },
  }
}
</script>

<style scoped>
</style>
