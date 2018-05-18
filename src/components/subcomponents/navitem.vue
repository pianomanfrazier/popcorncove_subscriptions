<template>
<router-link :to="item.link" class="menu-item">
  <v-list-tile class="menu-tile">
    <v-list-tile-action>
      <v-icon>fas fa-{{ item.icon }}</v-icon>
    </v-list-tile-action>
    <v-list-tile-content>
      <v-list-tile-title>
        {{ item.title }}
      </v-list-tile-title>
    </v-list-tile-content>
  </v-list-tile>
</router-link>
</template>

<script>
export default {
  name: 'navitem',
  props: ['item'],
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.router-link-active .menu-tile {
  background-color: rgba(0,0,0,0.1);
}
.menu-item {
  text-decoration: none;
}
.menu-tile:hover {
  background-color: rgba(0,0,0,0.1);
}
</style>
