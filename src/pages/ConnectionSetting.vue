<template>
    <q-page class="flex flex-center">
        <q-list>
            <q-item-label header>Данные о подключении</q-item-label>
            <q-item>
                <q-input
                    filled
                    v-model="ipText"
                    placeholder="192.168.0.X"
                    hint="Ip"
                >
                    <template v-slot:append>
                        <q-avatar>
                            <img
                                src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg"
                            />
                        </q-avatar>
                    </template>
                </q-input>
            </q-item>
            <q-item>
                <q-input
                    filled
                    v-model="portText"
                    placeholder="8765"
                    hint="Port"
                >
                    <template v-slot:append>
                        <q-avatar>
                            <img
                                src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg"
                            />
                        </q-avatar>
                    </template>
                </q-input>
            </q-item>
            <q-item>
              <q-btn label="Ввод!" @click="checkData" />
            </q-item>
        </q-list>
    </q-page>
</template>

<script>
export default {
    name: "ConnectionSetting",

    components: {},

    data() {
        return {
            ipText: "192.168.0.4",
            portText: "9090",
        };
    },

    methods: {
        checkData: function() {
            const regexIp = RegExp(
                "^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$"
            );
            const regexPort = RegExp("^[0-9]{1,4}$");
            if (regexIp.test(this.ipText) && regexPort.test(this.portText)) {
              this.$router.push({ path: `/control` });
            }
            else {
              alert("Данные были введены неверно")
            }
        },
    },
};
</script>

<style></style>
