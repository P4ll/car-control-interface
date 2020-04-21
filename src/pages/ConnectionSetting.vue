<template>
  <q-page class="flex flex-center">
    this is a connection setting page
    <q-input filled v-model="text" placeholder="192.168.0.X" hint="Ip" :dense="dense">
        <template v-slot:append>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
          </q-avatar>
        </template>
      </q-input>
      <br>
      <q-input filled v-model="text" placeholder="8765" hint="Port" :dense="dense">
        <template v-slot:append>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
          </q-avatar>
        </template>
      </q-input>
    <q-btn label="Управлять!" to="/control"/>
    <q-btn label="Проверка!" v-on:click="greet"/>
  </q-page>
</template>

<script>

export default {
    name: "ConnectionSetting",

    components: {
    },

    data() {
        return {
            
        };
    },

    methods: {
        
    },
};
</script>

<style></style>
