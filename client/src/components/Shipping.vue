<template>
  <v-card style="max-width: 55em; margin: auto;" flat>
    <v-card-title primary-title><h1 class="headline mb-0">Shipping Address for <em>{{ customer.name }}</em></h1></v-card-title>
      <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
          <v-flex xs12>
            <h2>Choose an Address</h2>
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

      </v-layout>
    </v-container>

    <v-card-actions>
      <v-btn @click.native="$emit('previous')">Previous</v-btn>
      <v-btn @click.native="$emit('cancel')" class="warning">Cancel</v-btn>
    </v-card-actions>

  </v-card>
</template>

<script>
let states = require('../assets/states_titlecase.json')

export default {
  name: 'shipping',
  props: ['customer'],
  data () {
    return {
      addresses: [],
      address: {},
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
      disableForm: false
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

<style>

</style>

