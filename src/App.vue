<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <MainScreen />
    </q-page-container>
  </q-layout>
</template>

<script>
import MainScreen from './components/MainScreen.vue'

export default {
  name: 'LayoutDefault',

  components: {
    MainScreen
  },

  data () {
    return {
      leftDrawerOpen: false,
    }
  }
}
</script>

<style>
</style>
