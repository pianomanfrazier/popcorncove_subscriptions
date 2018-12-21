<template>
    <v-card style="max-width: 55em; margin: auto;" flat>
      <v-card-title primary-title>
        <h1 class="headline mb-0">
        Subscription for <em>{{ customer.name }}</em>
        </h1>
      </v-card-title>

      <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
          <v-flex xs12>
            <h2>Choose a Subscription</h2>
          </v-flex>
          <v-flex xs4>
            <v-select
              v-model="subscription"
              :items="subscriptions"
              item-text="id"
              label="Subscription Number"
              autocomplete
              :filter="subscriptionfilter"
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
            <v-select
              v-model="select"
              :items="items"
              item-text="name"
              :rules="[v => !!v || 'Item is required']"
              label="Order Item"
              required
              :disabled="disableForm"
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
              :disabled="disableForm"
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
              :disabled="disableForm"
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
          <v-flex>
            <v-btn :disabled="!valid" v-if="!customer" @click="createSubscription();" style="float: left;" color="primary">Create Subscription</v-btn>
            <v-btn :disabled="!valid" v-if="customer && !disableForm" @click="updateSubscription(); disableForm = !disableForm;" style="float: left;">Update Subscription</v-btn>
            <v-btn v-if="customer && disableForm" @click="disableForm = !disableForm" style="float: left;">Edit Subscription</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>

    <v-card-actions>
      <v-btn @click.native="$emit('previous')">Previous</v-btn>
      <v-btn @click.native="$emit('cancel')" class="warning">Cancel</v-btn>
    </v-card-actions>

  </v-card>
</template>

<script>
import isFuture from 'date-fns/is_future'
import isAfter from 'date-fns/is_after'
import isBefore from 'date-fns/is_before'
import format from 'date-fns/format'

export default {
  name: 'subscription',
  props: ['customer'],
  data () {
    return {
      subscription: {},
      subscriptions: [],
      valid: false,
      disableForm: true,
      select: null,
      // TODO: get from the server
      items: [],
      startdate: '',
      enddate: '',
      startdatemenu: false,
      enddatemenu: false,
      notes: '',
      subscriptionfilter (item, queryText, itemText) {
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
    this.getItems()
  },
  methods: {
    getItems () {
      this.$http.get('/api/v1/item')
        .then(res => {
          this.items = res.data
        })
    },
    allowedStartDates (val) {
      // return false for any date before today
      return isFuture(val)
    },
    allowedEndDates (val) {
      // return false for any date before startdate
      return !isBefore(val, this.startdate) && isFuture(val)
    },
    updateSubscription () {

    },
    createSubscription () {
      if (this.$refs.form.validate()) {
        this.$http
          .post('/api/v1/subscription/' + this.customer.id, {
            itemID            : this.item.id,
            shippingAddressID : this.itemID,
            startDate         : this.itemID,
            stopDate          : this.itemID,
            note              : this.itemID
          })
          .then(res => {
            this.$toasted.show('Customer created')
            this.customer = res.data
            console.log(res)
          })
          .catch(err => {
            this.$toasted.err('Failed to create customer')
            console.log(err)
          })
      }

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
    startdate () {
      // if the startdate is set past the enddate reset it
      if (isAfter(this.startdate, this.enddate)) {
        this.enddate = ''
      }
    }
  }
}
</script>

<style>

</style>

