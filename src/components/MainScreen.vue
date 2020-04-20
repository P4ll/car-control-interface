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
            <q-btn @click="test2" />
            <q-img :src="mainImg"/>
            <!--<img :src="mainImg"/>-->
            <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA
    AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
        9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />
            <div id="pic"></div>
        </q-page>
    </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";
import { QImg } from 'quasar';

export default {
    name: "MainScreen",

    components: {
        ToggleButton,
        QImg
    },

    data() {
        return {
            leftDrawerOpen: false,
            useML: false,
            usePID: false,
            intervalId: null,
            socket: null,
            mainImg: "../assets/logo.png",
            msg: ""
        };
    },

    mounted() {
        this.test();
    },

    methods: {
        test() {
            this.socket = new WebSocket(
                "ws://localhost:8765"
            );

            this.socket.onopen = function() {
                alert("connected");
            };

            this.socket.onmessage = function(event) {
                console.log(`[message] Данные получены с сервера: ${event.data}`);
                // this.mainImg = "data:image/jpg;base64, " + event.data;
                this.msg = event.data;
                // this.msg = this.mainImg;
            };

            this.socket.onclose = function(event) {
                if (event.wasClean) {
                    alert(
                        `[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`
                    );
                } else {
                    // например, сервер убил процесс или сеть недоступна
                    // обычно в этом случае event.code 1006
                    alert("[close] Соединение прервано");
                }
                // clearInterval(this.intervalId);
            };

            this.socket.onerror = function(error) {
                alert(`[error] ${error.message}`);
                // clearInterval(this.intervalId);
            };
            //this.intervalId = setInterval(this.test2, 0);
        },
        test2() {
            await this.socket.send("1");
            this.mainImg = Math.random();
            this.mainImg = this.msg;
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
