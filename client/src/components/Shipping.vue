<template>
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

        <v-form ref="form" v-model="valid">
        <v-container>
          <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              v-model="street"
              label="Street Address"
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
          <v-flex xs4>
            <span v-if="!!address && customer.preferredShippingAddress === address.id">Preferred Address</span>
            <v-btn v-else :disabled="!(address && address.id)" @click="setPreferredAddress()">Set as Preferred Address</v-btn>
          </v-flex>
          <v-flex>
            <v-btn :disabled="!valid" v-if="!address" @click="createAddress();" style="float: left;" color="primary">Create Address</v-btn>
            <v-btn :disabled="!valid" v-if="address && !disableForm" @click="updateAddress(); disableForm = !disableForm;" style="float: left;">Update Address</v-btn>
            <v-btn v-if="address && disableForm" @click="disableForm = !disableForm" style="float: left;">Edit Address</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
      </v-form>

    <v-card-actions>
      <v-btn @click.native="$emit('previous')">Previous</v-btn>
      <v-btn :disabled="!address" @click.native="$emit('next')">Next</v-btn>
    </v-card-actions>

  </v-card>
</template>

<script>
let states = require('../assets/states_titlecase.json')

export default {
  name: 'shipping',
  props: ['customer', 'customers', 'address', 'addresses'],
  data () {
    return {
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
      valid: false,
      disableForm: true
    }
  },
  mounted () {
  },
  methods: {
    getAllAddresses () {
      if (this.customer && this.customer.id) {
        this.$http
          .get(`/api/v1/shippingaddress/${this.customer.id}`)
          .then(res => {
            // this.$toasted.show('Addresses fetched')
            this.$emit('update:addresses', res.data)
            let address = ''
            if (this.customer.preferredShippingAddress) {
              address = this.addresses.filter(el => el.id === this.customer.preferredShippingAddress)[0]
            } else if (this.addresses.length > 0) {
              address = this.addresses[0]
            }
            this.$emit('update:address', address)
            this.address = address
          })
          .catch(err => {
            // this.$toasted.error('Failed to fetch addresses')
            console.log(err)
          })
      }
    },
    createAddress () {
      if (this.$refs.form.validate()) {
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
            this.$emit('update:address', res.data)
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
      if (this.$refs.form.validate()) {
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
            this.$emit('update:address', res.data)
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
          this.$emit('update:customer', res.data)
          this.$http
            .get('/api/v1/customer')
            .then(res2 => {
              this.$emit('update:customers', res2.data)
            })
        })
        .catch(err => {
          this.$toasted.err('Failed to set preferred address')
          console.log(err)
        })
    },
  },
  watch: {
    customer (val) {
      this.$refs.form.reset()
      this.disableForm = false
      if (val) {
        this.getAllAddresses()
      }
    },
    address (val) {
      if (val) {
        this.disableForm = true
        this.street = val.address
        this.city = val.city
        this.state = val.state
        this.zip = val.zip
        // this.$emit('update:address', {
        //   address: this.street,
        //   city: this.city,
        //   state: this.state,
        //   zip: this.zip,
        //   id: this.address.id
        // })
      } else {
        this.$refs.form.reset()
        this.disableForm = false
        // this.$emit('update:address', null)
      }
    }
  }
}
</script>

<style>

</style>

