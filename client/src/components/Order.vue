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
    </v-stepper-header>
    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card>
          <v-card-title primary-title><h1 class="headline mb-0">Choose or Create a Customer</h1></v-card-title>

          <v-form style="max-width: 55em; margin: auto;" ref="form" v-model="valid">
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
                    item-text="fullname"
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
                    v-if="byField === 'address'"
                    v-model="customer"
                    :items="customers"
                    item-text="address"
                    label="Customer Address"
                    autocomplete
                    :filter="customeraddressfilter"
                    clearable
                  ></v-select>
                  <v-select
                    v-if="byField === 'customerID'"
                    v-model="customer"
                    :items="customers"
                    item-text="guid"
                    label="Customer ID"
                    autocomplete
                    :filter="customeridfilter"
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
                  <h2 class="pt-2">Customer Information</h2>
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    v-model="firstname"
                    :rules="nameRules"
                    label="First Name"
                    required
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs6>
                  <v-text-field
                    v-model="lastname"
                    :rules="nameRules"
                    label="Last Name"
                    required
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="E-mail"
                    required
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="phone"
                    :rules="phoneRules"
                    label="Phone Number"
                    mask="phone"
                    required
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="address"
                    label="Address"
                    :rules="[v => !!v || 'Address is required']"
                    required
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4>
                  <v-text-field
                    v-model="city"
                    label="City"
                    :rules="[v => !!v || 'City is required']"
                    required
                    :disabled="disableForm"
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
                    :disabled="disableForm"
                  ></v-select>
                </v-flex>
                <v-flex xs4>
                  <v-text-field
                    v-model="zip"
                    label="Zip Code"
                    required
                    :rules="zipRules"
                    :disabled="disableForm"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    v-model="notes"
                    label="Notes"
                    textarea
                    :disabled="disableForm"
                  >
                  </v-text-field>
                </v-flex>
                <v-flex>
                  <v-btn :disabled="!valid" v-if="!customer" @click="createCustomer();" style="float: left;" color="primary">Create Customer</v-btn>
                  <v-btn :disabled="!valid" v-if="customer && !disableForm" @click="updateCustomer(); disableForm = !disableForm;" style="float: left;">Update Customer</v-btn>
                  <v-btn v-if="customer && disableForm" @click="disableForm = !disableForm" style="float: left;">Edit Customer</v-btn>
                </v-flex>
              </v-layout>
            </v-container>
            </v-form>
          <v-card-actions>
            <v-btn :disabled="!customer" @click.native="stepper = 2">Next</v-btn>
            <v-btn @click.native="stepper = 1; clear()">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>
      <v-stepper-content step="2">
        <v-card v-if="!customer">
          <v-card-title primary-title>
            <h1 class="headline mb-0" style="color: red">
              No Customer Selected
            </h1>
          </v-card-title>
          <v-card-actions>
            <v-btn @click.native="stepper = 1">
              Previous
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-card v-if="customer">
          <v-card-title primary-title>
            <h1 class="headline mb-0">
            Subscription Selection for <em>{{ customer.name.first }} {{ customer.name.last }}</em>
            </h1>
          </v-card-title>
        <v-form ref="subform" v-model="subvalid">
        <v-container>
          <v-layout row wrap>
          <v-flex xs12>
            <v-select
              v-model="select"
              :items="items"
              :rules="[v => !!v || 'Item is required']"
              label="Order Item"
              required
            ></v-select>
          </v-flex>
          <v-flex xs5>
          <v-menu
            ref="startmenu"
            :close-on-content-click="false"
            v-model="startdatemenu"
            :nudge-right="40"
            :return-value.sync="startdate"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="startdateFormatted"
              label="Choose Start Month"
              prepend-icon="event"
              :rules="[v => !!v || 'Item is required']"
              required
              readonly
            ></v-text-field>
            <v-date-picker
              v-model="startdate"
              type="month"
              :allowed-dates="allowedStartDates"
              scrollable
            >
            </v-date-picker>
            <v-spacer></v-spacer>
            <v-btn flat color="primary" @click="startdatemenu = false">Cancel</v-btn>
            <v-btn flat color="primary" @click="$refs.startmenu.save(startdate)">OK</v-btn>
          </v-menu>
          </v-flex>
          <v-flex xs5 offset-xs1>
          <v-menu
            ref="endmenu"
            :close-on-content-click="false"
            v-model="enddatemenu"
            :nudge-right="40"
            :return-value.sync="enddate"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="enddateFormatted"
              label="Choose Ending Month"
              prepend-icon="event"
              :rules="[v => !!v || 'Item is required']"
              required
              readonly
            ></v-text-field>
            <v-date-picker
              v-model="enddate"
              type="month"
              :allowed-dates="allowedEndDates"
              scrollable
            >
            </v-date-picker>
            <v-spacer></v-spacer>
            <v-btn flat color="primary" @click="enddatemenu = false">Cancel</v-btn>
            <v-btn flat color="primary" @click="$refs.endmenu.save(enddate)">OK</v-btn>
          </v-menu>
          </v-flex>
        </v-layout>
      </v-container>
      </v-form>

      <v-card-actions>
        <v-btn @click.native="stepper = 1">Previous</v-btn>
        <v-btn @click.native="stepper = 1; clear()">Cancel</v-btn>
        <v-btn :disabled="!subvalid" color="primary" @click.native="placeOrder">Place Order</v-btn>
      </v-card-actions>

      </v-card>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>

  <v-dialog v-model="orderDialog" width="300px">
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
  </v-dialog>
</div>
</template>

<script>
let states = require('../assets/states_titlecase.json')
let customers = require('../assets/customers.json')

import isFuture from 'date-fns/is_future'
import isAfter from 'date-fns/is_after'
import isBefore from 'date-fns/is_before'
import format from 'date-fns/format'

export default {
  name: 'order',
  data () {
    return {
      orderDialog: false,
      stepper: 0,
      byField: 'email',
      byFields: [
        {
          text: 'By Email',
          value: 'email'
        },
        {
          text: 'By Name',
          value: 'name'
        },
        {
          text: 'By Address',
          value: 'address'
        },
        {
          text: 'By Customer ID',
          value: 'customerID'
        }
      ],
      customer: undefined,
      customers: [],
      customeraddressfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.address)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      customernamefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.fullname)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      customeridfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.guid)
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
      valid: false,
      firstname: '',
      lastname: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 10 || 'Name must be less than 10 characters'
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
      address: '',
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
      notes: '',
      select: null,
      items: [
        'Popcorn',
        'Treat',
        'Best of Both'
      ],
      startdate: '',
      enddate: '',
      startdatemenu: false,
      enddatemenu: false,
      disableForm: false,
      valid: false,
      subvalid: false
    }
  },
  mounted () {
    // customers.forEach( el => (
    //   el.fullname = `${el.name.last}, ${el.name.first}`
    // ))
    $http.get('/api/v1/customer')
      .then(res => {
        this.customers = res.data
      })
  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        this.$http.post('/api/submit', {
          //****************************/
          // customerId: this.customerId
          //****************************/
          // firstname: this.firstname,
          // lastname: this.lastname,
          // address: this.address,
          // city: this.city,
          // state: this.state,
          // zip: this.zip,
          // notes: this.notes,
          // email: this.email,
          // phone: this.phone,
          select: this.select,
          startdate: this.startdate,
          enddate: this.enddate
        })
      }
    },
    clear () {
      this.$refs.form.reset()
      this.$refs.subform.reset()
      this.startdate = ''
      this.enddate = ''
      this.byField = 'email'
    },
    createCustomer () {
      if (this.$refs.form.validate()) {
        this.$http.post('/api/v1/customer', {
          name: this.firstname + ' ' + this.lastname,
          email: this.email,
          phone: this.phone
        })
      }
    },
    updateCustomer () {
      if (this.$refs.form.validate()) {
        this.$http.put('/api/submit', {
          firstname: this.firstname,
          lastname: this.lastname,
          address: this.address,
          city: this.city,
          state: this.state,
          zip: this.zip,
          notes: this.notes,
          email: this.email,
          phone: this.phone
          // select: this.select,
          // startdate: this.startdate,
          // enddate: this.enddate
        })
      }
    },
    placeOrder () {
      this.orderDialog = true
    },
    allowedStartDates (val) {
      // return false for any date before today
      return isFuture(val)
    },
    allowedEndDates (val) {
      // return false for any date before startdate
      return !isBefore(val, this.startdate) && isFuture(val)
    }
  },
  computed: {
    startdateFormatted () {
      if (this.startdate) {
        return format(this.startdate, 'MMMM YYYY')
      }
      return ''
    },
    enddateFormatted () {
      if (this.enddate) {
        return format(this.enddate, 'MMMM YYYY')
      }
      return ''
    }
  },
  watch: {
    customer (val) {
      if (val) {
        this.firstname   = val.name.first
        this.lastname    = val.name.last
        this.address     = val.address
        this.city        = val.city
        this.state       = val.state
        this.zip         = val.zip
        this.email       = val.email
        this.phone       = val.phone
        this.notes       = val.notes

        this.disableForm = true
      } else {
        this.clear()
        this.disableForm = false
      }
    },
    startdate () {
      // if the startdate is set past the enddate reset it
      if (isAfter(this.startdate, this.enddate)) {
        this.enddate = ''
      }
    }
  }
}
</script>

<style scoped>
</style>
