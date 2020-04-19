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

        <q-toolbar-title>Панель управления автомоделью</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered content-class="bg-grey-2">
      <q-list>
        <q-item-label header>Settings</q-item-label>
        <q-item clickable @click="mlChange()">
          <q-item-section avatar>
            <toggle-button v-model="useML" />
          </q-item-section>
          <q-item-section>Распознавание лиц</q-item-section>
        </q-item>
        <q-item clickable @click="pidChange">
          <q-item-section avatar>
            <toggle-button v-model="usePID" />
          </q-item-section>
          <q-item-section>ПИД</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>
    <q-page class="flex flex-center">
      <img alt="Quasar logo" src="../assets/logo.png" />
    </q-page>
  </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";

export default {
  name: "MainScreen",

  components: {
    ToggleButton
  },

  data() {
    return {
      leftDrawerOpen: false,
      useML: false,
      usePID: false
    };
  },
  methods: [
    function created() {
      alert(11);
    },
    function mlChange() {
      alert(123);
      if (this.useML == false) this.useML = true;
      else this.useML = false;
    },
    function pidChange() {
      if (this.usePID == false) this.usePID = true;
      else this.usePID = false;
    }
  ]
};
</script>

<style>
</style>
