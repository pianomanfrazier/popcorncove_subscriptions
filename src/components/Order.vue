<template>
<div>
  <h1>Place an Order</h1>

    <v-form style="max-width: 55em; margin: auto;" ref="form" v-model="valid" lazy-validation>
      <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
          <v-flex xs12>
            <h2>Customer Information</h2>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              v-model="firstname"
              :rules="nameRules"
              label="First Name"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              v-model="lastname"
              :rules="nameRules"
              label="Last Name"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="email"
              :rules="emailRules"
              label="E-mail"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="address"
              label="Address"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs4>
            <v-text-field
              v-model="City"
              label="City"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs4>
            <v-select
              v-model="state"
              :items="states"
              :rules="[v => !!v || 'Item is required']"
              item-text="name"
              item-value="abbreviation"
              label="State"
              autocomplete
              :filter="statefilter"
              required
            ></v-select>
          </v-flex>
          <v-flex xs4>
            <v-text-field
              v-model="zip"
              label="Zip Code"
              required
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-divider></v-divider>
            <h2>Subscription Selection</h2>
          </v-flex>
          <v-flex xs6>
            <v-select
              v-model="select"
              :items="items"
              :rules="[v => !!v || 'Item is required']"
              label="Order Item"
              required
            ></v-select>
          </v-flex>
          <v-flex xs6></v-flex>
          <v-flex xs5>
          <v-menu
            ref="startmenu"
            :close-on-content-click="false"
            v-model="startdatemenu"
            :nudge-right="40"
            :return-value.sync="date"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="startdate"
              label="Choose Start Month"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker
              v-model="startdate"
              type="month"
              scrollable
            >
            </v-date-picker>
            <v-spacer></v-spacer>
            <v-btn flat color="primary" @click="startdatemenu = false">Cancel</v-btn>
            <v-btn flat color="primary" @click="$refs.startmenu.save(startdate)">OK</v-btn>
          </v-menu>
          </v-flex>
          <v-flex xs1></v-flex>
          <v-flex xs5>
          <v-menu
            ref="endmenu"
            :close-on-content-click="false"
            v-model="enddatemenu"
            :nudge-right="40"
            :return-value.sync="date"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="enddate"
              label="Choose Ending Month"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker
              v-model="enddate"
              type="month"
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

    <v-btn
      :disabled="!valid"
      @click="submit"
    >
      submit
    </v-btn>
    <v-btn @click="clear">clear</v-btn>
  </v-form>
</div>
</template>

<script>
let states = require('../assets/states_titlecase.json')

export default {
  name: '',
  data () {
    return {
      valid: false,
      firstname: '',
      lastname: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 10 || 'Name must be less than 10 characters'
      ],
      address: '',
      city: '',
      state: '',
      zip: '',
      states: states,
      statefilter (item, queryText, itemText) {
        const hasValue = val => val != null ? val : ''
        const text = hasValue(item.name)
        const query = hasValue(queryText)
        return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
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
      checkbox: false
    }
  },
  mounted () {
  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        // axios.post('/api/submit', {
        //   name: this.name,
        //   email: this.email,
        //   select: this.select,
        //   checkbox: this.checkbox
        // })
        console.log('form submit')
      }
    },
    clear () {
      this.$refs.form.reset()
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 2em;
  margin-bottom: 1em;
}
</style>
