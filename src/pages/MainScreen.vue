<template>
    <q-layout view="lHh Lpr lFf">
        <q-header elevated class="glossy">
            <q-toolbar class="bg-primary text-white">
                <q-btn
                    flat
                    dense
                    round
                    @click="leftDrawerOpen = !leftDrawerOpen"
                    aria-label="Menu"
                    icon="menu"
                />

                <q-toolbar-title center>Панель настроек</q-toolbar-title>
            </q-toolbar>
        </q-header>

        <q-drawer
            v-model="leftDrawerOpen"
            show-if-above
            bordered
            content-class="bg-grey-2"
        >
            <q-list>
                <q-item-label header>Настройки</q-item-label>
                <q-item clickable>
                    <q-item-section avatar>
                        <toggle-button v-model="useML" />
                    </q-item-section>
                    <q-item-section v-model="keyUpPressed"
                        >Распознавание лиц</q-item-section
                    >
                </q-item>
                <q-item clickable>
                    <q-item-section avatar>
                        <toggle-button v-model="usePID" />
                    </q-item-section>
                    <q-item-section>ПИД</q-item-section>
                </q-item>
                <q-item>
                    <q-btn label="Ввести новые данные о подключении" @click="getBack"/>
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
            mainImg: "",
            keyUpPressed: false,
            keyDownPressed: false,
            keyLeftPressed: false,
            keyRightPressed: false,
        };
    },

    created() {
        window.addEventListener('keydown', this.keyDown);
        window.addEventListener('keyup', this.keyUp);
    },

    beforeDestroy() {
        window.removeEventListener('keydown', this.keyDown);
        window.removeEventListener('keyup', this.keyUp);
    },

    mounted() {
        this.socketSetting();
    },

    methods: {
        getBack() {
            this.$router.push({ path: `/setting`});
            // Надо закрывать соединение и еще че нить поделать
        },
        keyDown(e) {
            if (e.key == "ArrowUp")
                this.keyUpPressed = true;
            else if (e.key == "ArrowDown")
                this.keyDownPressed = true;
            else if (e.key == "ArrowRight")
                this.keyRightPressed = true;
            else if (e.key == "ArrowLeft")
                this.keyLeftPressed = true;
        },
        keyUp(e) {
            if (e.key == "ArrowUp")
                this.keyUpPressed = false;
            else if (e.key == "ArrowDown")
                this.keyDownPressed = false;
            else if (e.key == "ArrowRight")
                this.keyRightPressed = false;
            else if (e.key == "ArrowLeft")
                this.keyLeftPressed = false;
        },
        socketSetting() {
            this.socket = new WebSocket(
                "ws://localhost:8765"
            );

            this.socket.onopen = function() {
                alert("connected");
            };

            this.socket.onmessage = function(event) {
                msg = "data:image/jpg;base64, " + event.data;
            };

            this.socket.onclose = function(event) {
                clearInterval(this.intervalId);
                if (event.wasClean) {
                    alert(
                        `[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`
                    );
                } else {
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
            // velocity(left, right) pid ml
            let rightSpeed = 0;
            let leftSpeed = 0;
            let outMessage = "";
            if (this.keyUpPressed)
                leftSpeed = 1, rightSpeed = 1;
            if (this.keyDownPressed)
                leftSpeed = -1, rightSpeed = -1;
            if (this.keyLeftPressed)
                rightSpeed = 1;
            if (this.keyRightPressed)
                leftSpeed = 1;
            outMessage = leftSpeed + " " + rightSpeed + " ";
            if (this.usePID)
                outMessage += 1;
            else
                outMessage += 0;
            if (this.useML)
                outMessage += " " + 1;
            else
                outMessage += " " + 0;
            this.socket.send(outMessage);
            console.log(outMessage);
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
