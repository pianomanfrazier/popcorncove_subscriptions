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
          <v-list>
            <v-list-tile v-for="item in items" :key="item.id">
              <v-list-tile-action>
                <v-checkbox v-model="selected" :value="item.id"></v-checkbox>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.name }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>

        <v-btn :disabled="!selected.length > 0" @click="deleteItems()" class="error">Delete Item<span v-if="selected.length > 1">s</span></v-btn>
        </v-flex>

      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name: 'items',
  data () {
    return {
      item: '',
      selected: [],
      items: []
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
    deleteItems () {
      this.$http
        .delete('/api/v1/item', selected)
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


