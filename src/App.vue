<template>
    <q-layout view="lHh Lpr lFf">
        <q-page-container>
            <q-page class="flex flex-center" v-if="isNotConnected">
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
            <q-layout view="lHh Lpr lFf" v-else>
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

                        <q-toolbar-title center
                            >Панель настроек</q-toolbar-title
                        >
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
                            <q-btn
                                label="Ввести новые данные о подключении"
                                @click="getBack"
                            />
                        </q-item>
                    </q-list>
                </q-drawer>
                <q-page class="flex flex-center">
                    <img :src="mainImg" />
                    <div id="pic"></div>
                </q-page>
            </q-layout>
        </q-page-container>
    </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";

var msg = "";
var isSocketConnected = false;

export default {
    name: "LayoutDefault",

    components: {
        ToggleButton,
    },

    data() {
        return {
            leftDrawerOpen: false,
            isNotConnected: true,
            // ipText: "192.168.0.4",
            ipText: "127.0.0.1",
            // portText: "9090",
            portText: "8765",
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

    methods: {
        getBackToSetting() {
            this.isNotConnected = true;
        },
        async checkData() {
            const regexIp = RegExp(
                "^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$"
            );
            const regexPort = RegExp("^[0-9]{1,4}$");
            if (regexIp.test(this.ipText) && regexPort.test(this.portText)) {
                await this.socketSetting();
                if (isSocketConnected) {
                    this.isNotConnected = false;
                    window.addEventListener("keydown", this.keyDown);
                    window.addEventListener("keyup", this.keyUp);
                } else {
                    alert("К сокету не удалось подключиться");
                }
            } else {
                alert("Данные были введены неверно");
            }
        },
        keyDown(e) {
            if (e.key == "ArrowUp") this.keyUpPressed = true;
            else if (e.key == "ArrowDown") this.keyDownPressed = true;
            else if (e.key == "ArrowRight") this.keyRightPressed = true;
            else if (e.key == "ArrowLeft") this.keyLeftPressed = true;
        },
        keyUp(e) {
            if (e.key == "ArrowUp") this.keyUpPressed = false;
            else if (e.key == "ArrowDown") this.keyDownPressed = false;
            else if (e.key == "ArrowRight") this.keyRightPressed = false;
            else if (e.key == "ArrowLeft") this.keyLeftPressed = false;
        },
        async socketSetting() {
            this.socket = await new WebSocket(
                "ws://" + this.ipText + ":" + this.portText
            );

            this.socket.onopen = function() {
                isSocketConnected = true;
            };

            this.socket.onmessage = function(event) {
                msg = "data:image/jpg;base64, " + event.data;
            };

            this.socket.onclose = function(event) {
                window.removeEventListener("keydown", this.keyDown);
                window.removeEventListener("keyup", this.keyUp);
                clearInterval(this.intervalId);
                this.isNotConnected = true;
                if (event.wasClean) {
                    alert(
                        `[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`
                    );
                } else {
                    alert("[close] Соединение прервано");
                }
            };

            this.socket.onerror = function(error) {
                this.isNotConnected = true;
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
            if (this.keyUpPressed) (leftSpeed = 1), (rightSpeed = 1);
            if (this.keyDownPressed) (leftSpeed = -1), (rightSpeed = -1);
            if (this.keyLeftPressed) rightSpeed = 1;
            if (this.keyRightPressed) leftSpeed = 1;
            outMessage = leftSpeed + " " + rightSpeed + " ";
            if (this.usePID) outMessage += 1;
            else outMessage += 0;
            if (this.useML) outMessage += " " + 1;
            else outMessage += " " + 0;
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
