<template>
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

    <v-form ref="form" v-model="valid">
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
          <v-flex>
            <v-btn :disabled="!valid" v-if="!customer" @click="createCustomer();" style="float: left;" color="primary">Create Customer</v-btn>
            <v-btn :disabled="!valid" v-if="customer && !disableForm" @click="updateCustomer(); disableForm = !disableForm;" style="float: left;">Update Customer</v-btn>
            <v-btn v-if="customer && disableForm" @click="disableForm = !disableForm" style="float: left;">Edit Customer</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>

    <v-card-actions class="mt-4">
      <v-btn :disabled="!customer" @click.native="$emit('next')">Next</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'customer',
  props: ['customers'],
  data () {
    return {
      customer: null,
      byField: 'name',
      byFields: [
        'name',
        'email',
        'phone'
      ],
      valid: false,
      disableForm: false,
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
      customeremailfilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.phone)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
    }
  },
  mounted () {
    this.getAllCustomers()
  },
  methods: {
    getAllCustomers () {
      this.$http.get('/api/v1/customer')
        .then(res => {
          this.$emit('update:customers', res.data)
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
            this.$emit('update:customer', res.data)
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
            this.$emit('update:customer', res.data)
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
        this.disableForm = true
        this.$emit('update:customer', this.customer)
      } else {
        this.$refs.form.reset()
        this.disableForm = false
        this.$emit('update:customer', {})
      }
    }
  }
}
</script>

<style>

</style>

