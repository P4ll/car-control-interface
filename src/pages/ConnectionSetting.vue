<template>
  <q-page class="flex flex-center">
    this is a connection setting page
    <q-input filled id= "IP" v-model="text" placeholder="192.168.0.X" hint="Ip" :dense="dense">
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
    <q-btn label="Проверка!" v-on:click="checkData"/>
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
        checkData: function(event) {
            alert('Привет')
            const ip = '192.168.0.4a';
            const port = '8q';
            const regexIp = RegExp('^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$');
            const regexPort = RegExp('^[0-9]{1,4}$')
            alert(regexIp.test(ip));
            alert(regexPort.test(port));
            if (event) {
              console.log(event.target.tagName)
            }
        },
    },
};
</script>

<style></style>
