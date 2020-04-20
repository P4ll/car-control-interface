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
                        <toggle-button v-model="useML" />
                    </q-item-section>
                    <q-item-section
                        >Распознавание лиц {{ useML }}</q-item-section
                    >
                </q-item>
                <q-item clickable>
                    <q-item-section avatar>
                        <toggle-button v-model="usePID" />
                    </q-item-section>
                    <q-item-section>ПИД</q-item-section>
                </q-item>
            </q-list>
        </q-drawer>
        <q-page class="flex flex-center">
            <img :src="mainImg"/>
            <div id="pic"></div>
        </q-page>
    </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";
var msg = "";

export default {
    name: "MainScreen",

    components: {
        ToggleButton,
    },

    data() {
        return {
            leftDrawerOpen: false,
            useML: false,
            usePID: false,
            intervalId: null,
            socket: null,
            mainImg: ""
        };
    },

    mounted() {
        this.socketSetting();
    },

    methods: {
        socketSetting() {
            this.socket = new WebSocket(
                "ws://localhost:8765"
            );

            this.socket.onopen = function() {
                alert("connected");
            };

            this.socket.onmessage = function(event) {
                console.log("data:image/jpg;base64, " + event.data);
                msg = "data:image/jpg;base64, " + event.data;
            };

            this.socket.onclose = function(event) {
                clearInterval(this.intervalId);
                if (event.wasClean) {
                    alert(
                        `[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`
                    );
                } else {
                    // например, сервер убил процесс или сеть недоступна
                    // обычно в этом случае event.code 1006
                    alert("[close] Соединение прервано");
                }
            };

            this.socket.onerror = function(error) {
                clearInterval(this.intervalId);
                alert(`[error] ${error.message}`);
            };
            this.intervalId = setInterval(this.sendingMessage, 0);
        },
        sendingMessage() {
            this.socket.send("1");
            this.mainImg = msg;
        },
        mlChange() {
            if (this.useML == false) this.useML = true;
            else this.useML = false;
        },
        pidChange() {
            if (this.usePID == false) this.usePID = true;
            else this.usePID = false;
        },
    },
};
</script>

<style></style>
