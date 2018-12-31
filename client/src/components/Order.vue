<template>
<div>
  <v-stepper v-model="stepper">
    <v-stepper-header>
      <v-stepper-step :complete="stepper > 1" step="1">
        Choose or create a customer
      </v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="stepper > 2" step="2">
        Choose a Shipping Address
      </v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="stepper > 3" step="3">
        Create or Change a Subscription
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
                <v-autocomplete
                  v-if="byField === 'name'"
                  v-model="customer"
                  :items="customers"
                  :return-object="true"
                  item-text="name"
                  label="Customer Name"
                  :filter="customernamefilter"
                  clearable
                ></v-autocomplete>
                <v-autocomplete
                  v-if="byField === 'email'"
                  v-model="customer"
                  :items="customers"
                  :return-object="true"
                  item-text="email"
                  label="Customer Email"
                  :filter="customeremailfilter"
                  clearable
                ></v-autocomplete>
                <v-autocomplete
                  v-if="byField === 'phone'"
                  v-model="customer"
                  :items="customers"
                  :return-object="true"
                  item-text="phone"
                  label="Customer Phone"
                  :filter="customerphonefilter"
                  clearable
                ></v-autocomplete>
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
        <v-card v-if="customer" style="max-width: 55em; margin: auto;" flat>
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
                    :return-object="true"
                    item-text="address"
                    label="Address"
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
                <v-flex xs4>
                  <span v-if="!!address && customer.preferredShippingAddress === address.id">Preferred Address</span>
                  <v-btn v-else :disabled="!(address && address.id)" @click="setPreferredAddress()">Set as Preferred Address</v-btn>
                </v-flex>
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
                  <v-autocomplete
                    v-model="state"
                    :items="states"
                    :rules="[v => !!v || 'Item is required']"
                    item-text="name"
                    item-value="name"
                    label="State"
                    :filter="statefilter"
                    required
                    :disabled="disableShippingForm"
                  ></v-autocomplete>
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
        <v-card style="max-width: 55em; margin: auto;" flat>
          <v-card-title primary-title>
            <h1 class="headline mb-0">
            Subscription for <em v-if="customer">{{ customer.name }}</em>
            </h1>
          </v-card-title>

          <v-container grid-list-md text-xs-center>
            <v-layout row wrap>
              <v-flex xs12>
                <h2>Choose a Subscription</h2>
              </v-flex>
              <v-flex xs4>
                <v-autocomplete
                  v-model="subscription"
                  :items="subscriptions"
                  item-text="id"
                  label="Subscription Number"
                  :filter="subscriptionfilter"
                  :return-object="true"
                  clearable
                ></v-autocomplete>
              </v-flex>
            <v-flex xs12>
              <v-divider></v-divider>
            </v-flex>
            </v-layout>
          </v-container>

          <v-form ref="subscriptionForm" v-model="valid">
            <v-container>
              <v-layout row wrap>
              <v-flex xs12>
                <v-autocomplete
                  v-model="item"
                  :items="items"
                  item-text="name"
                  :rules="[v => !!v || 'Item is required']"
                  :return-object="true"
                  label="Order Item"
                  required
                  :disabled="disableForm"
                ></v-autocomplete>
              </v-flex>
              <v-flex xs5>
              <v-menu
                ref="startmenu"
                :close-on-content-click="false"
                v-model="startDatemenu"
                :nudge-right="40"
                :return-value.sync="startDate"
                lazy
                transition="scale-transition"
                offset-y
                full-width
                max-width="290px"
                min-width="290px"
              >
                <v-text-field
                  slot="activator"
                  v-model="startDateFormatted"
                  label="Choose Start Month"
                  prepend-icon="event"
                  :rules="[v => !!v || 'Item is required']"
                  :disabled="disableForm"
                  required
                  readonly
                ></v-text-field>
                <v-date-picker
                  v-model="startDate"
                  type="month"
                  :allowed-dates="allowedStartDates"
                  scrollable
                >
                </v-date-picker>
                <v-spacer></v-spacer>
                <v-btn flat color="primary" @click="startDatemenu = false">Cancel</v-btn>
                <v-btn flat color="primary" @click="$refs.startmenu.save(startDate)">OK</v-btn>
              </v-menu>
              </v-flex>
              <v-flex xs5 offset-xs1>
              <v-menu
                ref="endmenu"
                :close-on-content-click="false"
                v-model="stopDatemenu"
                :nudge-right="40"
                :return-value.sync="stopDate"
                lazy
                transition="scale-transition"
                offset-y
                full-width
                max-width="290px"
                min-width="290px"
              >
                <v-text-field
                  slot="activator"
                  v-model="stopDateFormatted"
                  label="Choose Ending Month"
                  prepend-icon="event"
                  :rules="[v => !!v || 'Item is required']"
                  :disabled="disableForm"
                  required
                  readonly
                ></v-text-field>
                <v-date-picker
                  v-model="stopDate"
                  type="month"
                  :allowed-dates="allowedEndDates"
                  scrollable
                >
                </v-date-picker>
                <v-spacer></v-spacer>
                <v-btn flat color="primary" @click="stopDatemenu = false">Cancel</v-btn>
                <v-btn flat color="primary" @click="$refs.endmenu.save(stopDate)">OK</v-btn>
              </v-menu>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  v-model="note"
                  label="Notes"
                  :disabled="disableForm"
                ></v-textarea>
              </v-flex>
              <v-flex>
                <v-btn :disabled="!valid" v-if="!subscription" @click="createSubscription();" style="float: left;" color="primary">Create Subscription</v-btn>
                <v-btn :disabled="!valid" v-if="subscription && !disableForm" @click="updateSubscription(); disableForm = !disableForm;" style="float: left;">Update Subscription</v-btn>
                <v-btn v-if="subscription && disableForm" @click="disableForm = !disableForm" style="float: left;">Edit Subscription</v-btn>
              </v-flex>
            </v-layout>
            </v-container>
          </v-form>

          <v-card-actions>
            <v-btn @click.native="stepper = 2">Previous</v-btn>
            <v-btn @click.native="stepper = 1;" class="primary">Go Back to Beginning</v-btn>
            <v-btn v-if="customer && item && address && subscription" @click.native="orderDialog = true" class="success">Preview Subscription</v-btn>
          </v-card-actions>

        </v-card>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>

  <v-dialog v-model="orderDialog" v-if="customer && item && address && subscription" width="300px">
    <v-card tile>
      <v-card-text>
        <h2>Subscription Preview</h2>
        <p>
        <b>Customer:</b> {{ customer.name }}<br>
        <b>Item:</b> {{ item.name }} <br>
        <b>Subscription Dates:</b> {{ startDate | formatDate }} to {{ stopDate | formatDate }}
        <b>Shipping Address:</b> {{ address.address }}, {{ address.city }}, {{ address.state }} {{ address.zip}}
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="orderDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</div>
</template>

<script>
import isFuture from 'date-fns/is_future'
import isAfter from 'date-fns/is_after'
import isBefore from 'date-fns/is_before'
import format from 'date-fns/format'

let states = require('../assets/states_titlecase.json')

export default {
  name: 'order',
  data () {
    return {
      customer: undefined,
      customers: [],
      address: undefined,
      addresses: [],
      subscription: undefined,
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
      disableShippingForm: false,
      // Subscription Data
      valid: false,
      disableForm: false,
      item: undefined,
      items: [],
      startDate: '',
      stopDate: '',
      startDatemenu: false,
      stopDatemenu: false,
      note: '',
      subscriptionfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.id)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
    }
  },
  mounted () {
    this.getAllCustomers()
    this.getItems()
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
    getAllAddresses (callback) {
      if (this.customer && this.customer.id) {
        this.$http
          .get(`/api/v1/shippingaddress/${this.customer.id}`)
          .then(res => {
            // this.$toasted.show('Addresses fetched')
            this.addresses = res.data
            if (callback) {
              callback()
            }
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
      if (this.$refs.shippingForm && this.$refs.shippingForm.validate()) {
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
    getItems () {
      this.$http.get('/api/v1/item')
        .then(res => {
          this.items = res.data
        })
        .catch(err => {
          this.$toasted.error('Failed to fetch subscription items')
        })
    },
    getAllSubscriptions (callback) {
      this.$http.get(`/api/v1/subscription/${this.customer.id}`)
        .then(res => {
          this.subscriptions = res.data
          if (callback) {
            callback()
          }
        })
        .catch(err => {
          this.$toasted.error('Failed to fetch subscriptions')
        })
    },
    allowedStartDates (val) {
      // return false for any date before today
      return isFuture(val)
    },
    allowedEndDates (val) {
      // return false for any date before startDate
      return !isBefore(val, this.startDate) && isFuture(val)
    },
    updateSubscription () {
      if (this.$refs.subscriptionForm.validate()) {
        this.$http
          .put(`/api/v1/subscription/${this.subscription.id}`, {
            customerID        : this.customer.id,
            itemID            : this.item.id,
            shippingAddressID : this.address.id,
            startDate         : this.startDate,
            stopDate          : this.stopDate,
            note              : this.note
          })
          .then(res => {
            this.$toasted.show('Subscription updated')
            this.subscription = res.data
            this.getAllSubscriptions()
          })
          .catch(err => {
            this.$toasted.err('Failed to update subscription')
            console.log(err)
          })
      }
    },
    createSubscription () {
      if (this.$refs.subscriptionForm.validate()) {
        this.$http
          .post('/api/v1/subscription', {
            customerID        : this.customer.id,
            itemID            : this.item.id,
            shippingAddressID : this.address.id,
            startDate         : this.startDate,
            stopDate          : this.stopDate,
            note              : this.note
          })
          .then(res => {
            this.$toasted.show('Subscription created')
            this.subscription = res.data
            this.getAllSubscriptions()
          })
          .catch(err => {
            this.$toasted.err('Failed to create subscription')
            console.log(err)
          })
      }
    }
  },
  computed: {
    startDateFormatted: {
      get () {
        if (this.startDate) {
          return format(this.startDate, 'MMMM YYYY')
        }
        return ''
      },
      set (newValue) {
        return format(newValue, 'YYYY-MM')
      }
    },
    stopDateFormatted: {
      get () {
      if (this.stopDate) {
        return format(this.stopDate, 'MMMM YYYY')
      }
      return
      },
      set (newValue) {
        return format(newValue, 'YYYY-MM')
      }
    }
  },
  watch: {
    customer (val) {
      if (val) {
        this.name = val.name
        this.email = val.email
        this.phone = val.phone
        this.disableCustomerForm = true
        this.getAllAddresses(() => {
          if (this.customer.preferredShippingAddress) {
            this.address = this.addresses.filter(el => el.id === this.customer.preferredShippingAddress)[0]
          } else if (this.addresses.length > 0) {
            this.address = this.addresses[0]
          }
        })
      } else {
        // reset all the forms ahead of it
        this.$refs.customerForm.reset()
        this.disableCustomerForm = false

        if (this.$refs.shippingForm)
          this.$refs.shippingForm.reset()
        this.disableShippingForm = false

        if (this.$refs.subscriptionForm)
          this.$refs.subscriptionForm.reset()
        this.disableForm = false

        this.customer = undefined
        this.address = undefined
        this.subscription = undefined
      }
    },
    address (val) {
      if (val) {
        this.disableShippingForm = true
        this.street = val.address
        this.city = val.city
        this.state = val.state
        this.zip = val.zip
        this.getAllSubscriptions(() => {
          if (this.subscriptions.length > 0) {
            this.subscription = this.subscriptions[0]
          }
        })
      } else {
        this.$refs.shippingForm.reset()
        this.disableShippingForm = false

        if (this.$refs.subscriptionForm)
          this.$refs.subscriptionForm.reset()
        this.disableForm = false

        this.address = undefined
        this.subscription = undefined
      }
    },
    subscription (val) {
      if (val) {
        this.items.forEach(el => {
          if (el.id === val.itemID) {
            this.item = el
          }
        })
        this.disableForm = true
        this.stopDate = val.stopDate
        this.startDate = val.startDate
        this.note = val.note
      } else {
        this.$refs.subscriptionForm.reset()
        this.disableForm = false
        this.subscription = undefined
        this.startDate = ''
        this.stopDate = ''
      }
    },
    startDate () {
      // if the startDate is set past the stopDate reset it
      if (isAfter(this.startDate, this.stopDate)) {
        this.stopDate = ''
      }
    }
  }
}
</script>

<style scoped>
</style>
