<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="glossy">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Settings</q-item-label>
        <q-item clickable>
          <q-item-section avatar>
            <toggle-button @change="mlChange" v-model="useML" />
          </q-item-section>
          <q-item-section>
            Распознавание лиц {{ useML }}
          </q-item-section>
        </q-item>
        <q-item clickable>
          <q-item-section avatar>
            <toggle-button @change="mlChange" v-model="usePID" />
          </q-item-section>
          <q-item-section>
            ПИД {{ usePID }}
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <MainScreen />
    </q-page-container>
  </q-layout>
</template>

<script>
import MainScreen from './components/MainScreen.vue'
import { ToggleButton } from 'vue-js-toggle-button'

export default {
  name: 'LayoutDefault',

  components: {
    MainScreen,
    ToggleButton
  },

  data () {
    return {
      leftDrawerOpen: false,
      useML: false,
      usePID: false
    }
  },
  methods: [
    function mlChange() {

    }
  ]
}
</script>

<style>
</style>
