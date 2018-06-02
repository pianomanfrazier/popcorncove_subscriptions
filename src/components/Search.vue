<template>
<div>
  <h1>Search the Database</h1>
  <SearchBar v-model="searchQuery"></SearchBar>
  {{ searchQuery }}
</div>
</template>

<script>
import SearchBar from './subcomponents/SearchBar'

export default {
  name: '',
  components: {
    SearchBar
  },
  data () {
    return {
      searchQuery: ''
    }
  }
}
</script>

<style scoped>
</style>
