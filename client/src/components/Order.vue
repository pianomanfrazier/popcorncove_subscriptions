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

          <v-form ref="customerForm" v-model="validCustomer">
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
      <v-card style="max-width: 55em; margin: auto;" flat>
          <v-card-title primary-title><h1 class="headline mb-0">Shipping Address for <em>{{ customer.name }}</em></h1></v-card-title>
            <v-container grid-list-md text-xs-center>
              <v-layout row wrap>
                <v-flex xs12>
                  <h2>Choose a Shipping Address</h2>
                </v-flex>
                <v-flex xs12>
                  <v-select
                    v-model="address"
                    :items="addresses"
                    item-text="address"
                    label="Address"
                    autocomplete
                    :filter="addressfilter"
                    clearable
                  ></v-select>
                </v-flex>
                <v-flex xs12>
                  <v-divider></v-divider>
                </v-flex>
              </v-layout>
            </v-container>

              <v-form ref="shippingForm" v-model="validShipping">
              <v-container>
                <v-layout row wrap>
                <v-flex xs12>
                  <v-text-field
                    v-model="street"
                    label="Street Address"
                    :rules="[v => !!v || 'Address is required']"
                    required
                    :disabled="disableShippingForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4>
                  <v-text-field
                    v-model="city"
                    label="City"
                    :rules="[v => !!v || 'City is required']"
                    required
                    :disabled="disableShippingForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4>
                  <v-select
                    v-model="state"
                    :items="states"
                    :rules="[v => !!v || 'Item is required']"
                    item-text="name"
                    item-value="name"
                    label="State"
                    autocomplete
                    :filter="statefilter"
                    required
                    :disabled="disableShippingForm"
                  ></v-select>
                </v-flex>
                <v-flex xs4>
                  <v-text-field
                    v-model="zip"
                    label="Zip Code"
                    required
                    :rules="zipRules"
                    :disabled="disableShippingForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4>
                  <span v-if="!!address && customer.preferredShippingAddress === address.id">Preferred Address</span>
                  <v-btn v-else :disabled="!(address && address.id)" @click="setPreferredAddress()">Set as Preferred Address</v-btn>
                </v-flex>
                <v-flex>
                  <v-btn :disabled="!validShipping" v-if="!address" @click="createAddress();" style="float: left;" color="primary">Create Address</v-btn>
                  <v-btn :disabled="!validShipping" v-if="address && !disableShippingForm" @click="updateAddress(); disableShippingForm = !disableShippingForm;" style="float: left;">Update Address</v-btn>
                  <v-btn v-if="address && disableShippingForm" @click="disableShippingForm = !disableShippingForm" style="float: left;">Edit Address</v-btn>
                </v-flex>
              </v-layout>
            </v-container>
            </v-form>

          <v-card-actions>
            <v-btn @click.native="stepper = 1">Previous</v-btn>
            <v-btn :disabled="!address" @click.native="stepper = 3">Next</v-btn>
          </v-card-actions>

        </v-card>
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
let states = require('../assets/states_titlecase.json')
import Subscription from './Subscription'

export default {
  name: 'order',
  components: {
    Subscription,
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
      street: '',
      city: '',
      state: '',
      zip: '',
      zipRules: [
        v => !!v || 'Zip Code is required',
        v => /(^\d{5}$)|(^\d{5}-\d{4}$)/.test(v) || 'Zip Code must be valid'
      ],
      states: states,
      statefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.name)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      addressfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.address)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      phonefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.phone)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      validShipping: false,
      disableShippingForm: true
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
      if (this.$refs.customerForm.validate()) {
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
      if (this.$refs.customerForm.validate()) {
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
    },
    // Shipping Methods
    getAllAddresses () {
      if (this.customer && this.customer.id) {
        this.$http
          .get(`/api/v1/shippingaddress/${this.customer.id}`)
          .then(res => {
            // this.$toasted.show('Addresses fetched')
            this.addresses = res.data
            let address = ''
            if (this.customer.preferredShippingAddress) {
              address = this.addresses.filter(el => el.id === this.customer.preferredShippingAddress)[0]
            } else if (this.addresses.length > 0) {
              address = this.addresses[0]
            }
            this.address = address 
          })
          .catch(err => {
            // this.$toasted.error('Failed to fetch addresses')
            console.log(err)
          })
      }
    },
    createAddress () {
      if (this.$refs.customerForm.validate()) {
        this.$http
          .post('/api/v1/shippingaddress', {
            customerID  : this.customer.id,
            address     : this.street,
            city        : this.city,
            state       : this.state,
            zip         : this.zip
          })
          .then(res => {
            this.$toasted.show('Address created')
            this.address = res.data
            this.getAllAddresses()
          })
          .catch(err => {
            this.$toasted.err('Failed to create address')
            console.log(err)
          })
      }
    },
    updateAddress () {
      if (this.$refs.shippingForm.validate()) {
        this.$http
          .put(`/api/v1/shippingaddress/${this.address.id}`, {
            customerID  : this.customer.id,
            address     : this.street,
            city        : this.city,
            state       : this.state,
            zip         : this.zip
          })
          .then(res => {
            this.$toasted.show('Address updated')
            this.address = res.data
            this.getAllAddresses()
          })
          .catch(err => {
            this.$toasted.err('Failed to update address')
            console.log(err)
          })
      }
    },
    setPreferredAddress () {
      this.$http
        .put(`/api/v1/customer/${this.customer.id}`, {
          name: this.customer.name,
          phone: this.customer.phone,
          email: this.customer.email,
          preferredShippingAddress: this.address.id
        })
        .then(res => {
          this.$toasted.show('Preferred address set')
          this.customer = res.data
          this.$http
            .get('/api/v1/customer')
            .then(res2 => {
              this.customers = res2.data
            })
        })
        .catch(err => {
          this.$toasted.err('Failed to set preferred address')
          console.log(err)
        })
    },
    // Subscription Methods
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
        this.getAllAddresses()
      } else {
        this.$refs.customerForm.reset()
        this.disableCustomerForm = false
      }
    },
    address (val) {
      if (val) {
        this.disableShippingForm = true
        this.street = val.address
        this.city = val.city
        this.state = val.state
        this.zip = val.zip
      } else {
        this.$refs.shippingForm.reset()
        this.disableShippingForm = false
      }
    }
  }
}
</script>

<style scoped>
</style>
