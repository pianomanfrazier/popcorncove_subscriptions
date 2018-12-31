<template>
  <v-card  flat>
    <v-card-title primary-title><h1 class="headline mb-0">Add Subscription Items</h1></v-card-title>

    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex xs4 offset-xs4>
          <v-text-field
            v-model="item"
            label="New item"
          ></v-text-field>
          <v-btn :disabled="item.length === 0" @click="addItem()">Add Item</v-btn>
        </v-flex>
        <v-flex xs4 offset-xs4>
          <h2>Subscription Items</h2>
          <v-list>
            <v-list-tile v-for="item in items" :key="item.id">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.name }}
                </v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn @click="deleteDialog = true; deleteID = item.id; migrateID = undefined" class="error">Delete Item</v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>

        </v-flex>

      </v-layout>
    </v-container>

    <v-dialog v-model="deleteDialog" width="300px">
      <v-card tile>
        <v-alert
          :value="true"
          type="warning"
        >
        This action cannot be undone.
        </v-alert>
        <v-card-text>
          Where would you like to migrate existing subscriptions with this item?
        </v-card-text>
        <v-card-actions>
          <v-radio-group v-model="migrateID">
            <v-radio
              v-for="item in items.filter(el => el.id !== deleteID)"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></v-radio>
          </v-radio-group>
        </v-card-actions>
        <v-card-actions>
          <v-btn @click="deleteDialog = false; deleteID = undefined; migrateID = undefined;">Cancel</v-btn>
          <v-btn :disabled="!migrateID" @click="deleteItems(deleteID, migrateID)" class="error">Delete Item</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-card>
</template>

<script>
export default {
  name: 'items',
  data () {
    return {
      item: '',
      items: [],
      radioGroup: undefined,
      deleteDialog: false,
      deleteID: undefined,
      migrateID: undefined,
    }
  },
  mounted () {
    this.getItems()
  },
  methods: {
    addItem () {
      this.$http
        .post('/api/v1/item', {
          name: this.item
        })
        .then(res => {
          this.$toasted.show('Added a new item')
          this.item = ''
          this.getItems()
        })
        .catch(err => {
          this.$toasted.error('Failed to add new item')
        })
    },
    deleteItems (id, migrateID) {
      this.$http
        .delete(`/api/v1/item/${id}`, {
          params: {migrate: migrateID}
        })
        .then(res => {
          this.$toasted.show('Item deleted')
          this.getItems()
          this.deleteDialog = false
        })
        .catch(err => {
          this.$toasted.error('Failed to delete item')
        })
    },
    getItems () {
      this.$http
        .get('/api/v1/item')
        .then(res => {
          this.items = res.data
        })
        .catch(err => {
          this.$toasted.error('Unable to fetch subscription items')
        })
    }
  }
}
</script>

<style>

</style>


