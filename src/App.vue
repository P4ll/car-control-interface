<template>
    <q-layout view="lHh Lpr lFf">
        <q-page-container>
            <q-page class="flex flex-center" v-if="isNotConnected">
                <q-list>
                    <q-item-label header>Данные о подключении</q-item-label>
                    <q-item>
                        <q-input
                            label="IP"
                            filled
                            v-model="ipText"
                            placeholder="192.168.0.X"
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
                            label="Port"
                            filled
                            v-model="portText"
                            placeholder="8765"
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
                        <q-btn label="Подключиться" @click="checkData" />
                    </q-item>
                </q-list>
            </q-page>
            <q-page class="flex flex-center" v-else>
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
                                @click="getBackToSetting"
                            />
                        </q-item>
                    </q-list>
                </q-drawer>
                <q-page class="flex flex-center">
                    <q-list>
                        <q-item>
                            <div id="pic" class="row">
                                <div class="col">
                                    <img :src="mainImg" class="img-m" />
                                </div>
                            </div>
                        </q-item>
                        <q-item>
                            <q-item-section class="arrow">
                                <div class="arrow arrow-holder">
                                    <div class="row">
                                        <div class="col"></div>
                                        <div class="col">
                                            <q-btn
                                                round
                                                :color="upCol"
                                                icon="navigation"
                                                class="arrow arrow-up"
                                            />
                                        </div>
                                        <div class="col"></div>
                                    </div>
                                    <div class="row">
                                        <div class="col">
                                            <q-btn
                                                round
                                                :color="leftCol"
                                                icon="navigation"
                                                class="arrow arrow-right"
                                            />
                                        </div>
                                        <div class="col">
                                            <q-btn
                                                round
                                                :color="downCol"
                                                icon="navigation"
                                                class="arrow arrow-down"
                                            />
                                        </div>
                                        <div class="col">
                                            <q-btn
                                                round
                                                :color="rightCol"
                                                icon="navigation"
                                                class="arrow arrow-left"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </q-item-section>
                        </q-item>
                    </q-list>
                </q-page>
                <q-page class="flex flex-center"> </q-page>
            </q-page>
        </q-page-container>
    </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";
var msg = "";
var intervalId = null;

export default {
    name: "LayoutDefault",
    components: {
        ToggleButton,
    },
    beforeMount() {
        document.title = "Панель управления";
    },
    mounted() {
        this.upCol = this.passiveCol;
        this.downCol = this.passiveCol;
        this.rightCol = this.passiveCol;
        this.leftCol = this.passiveCol;
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
            socket: null,
            mainImg: "",
            keyUpPressed: false,
            keyDownPressed: false,
            keyLeftPressed: false,
            keyRightPressed: false,
            activeCol: "blue",
            passiveCol: "grey",
            upCol: this.passiveCol,
            downCol: this.passiveCol,
            rightCol: this.passiveCol,
            leftCol: this.passiveCol,
        };
    },
    methods: {
        getBackToSetting() {
            window.removeEventListener("keydown", this.keyDown);
            window.removeEventListener("keyup", this.keyUp);
            clearInterval(intervalId);
            this.isNotConnected = true;
            this.socket.close();
        },
        showNegNotify(outMsg) {
            this.$q.notify({
                type: "negative",
                message: outMsg,
            });
        },
        checkData() {
            const regexIp = RegExp(
                "^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$"
            );
            const regexPort = RegExp("^[0-9]{1,4}$");
            if (regexIp.test(this.ipText) && regexPort.test(this.portText)) {
                this.socketSetting();
            } else {
                this.showNegNotify("Данные были введены неверно");
            }
        },
        keyDown(e) {
            if (e.key == "ArrowUp") {
                this.keyUpPressed = true;
                this.upCol = this.activeCol;
            } else if (e.key == "ArrowDown") {
                this.keyDownPressed = true;
                this.downCol = this.activeCol;
            } else if (e.key == "ArrowRight") {
                this.keyRightPressed = true;
                this.rightCol = this.activeCol;
            } else if (e.key == "ArrowLeft") {
                this.keyLeftPressed = true;
                this.leftCol = this.activeCol;
            }
        },
        keyUp(e) {
            if (e.key == "ArrowUp") {
                this.keyUpPressed = false;
                this.upCol = this.passiveCol;
            } else if (e.key == "ArrowDown") {
                this.keyDownPressed = false;
                this.downCol = this.passiveCol;
            } else if (e.key == "ArrowRight") {
                this.keyRightPressed = false;
                this.rightCol = this.passiveCol;
            } else if (e.key == "ArrowLeft") {
                this.keyLeftPressed = false;
                this.leftCol = this.passiveCol;
            }
        },
        socketSetting() {
            this.socket = new WebSocket(
                "ws://" + this.ipText + ":" + this.portText
            );
            this.socket.onopen = () => {
                this.isNotConnected = false;
                window.addEventListener("keydown", this.keyDown);
                window.addEventListener("keyup", this.keyUp);
                intervalId = setInterval(this.sendingMessage, 1);
            };
            this.socket.onmessage = (event) => {
                msg = "data:image/jpg;base64, " + event.data;
            };
            this.socket.onclose = (event) => {
                window.removeEventListener("keydown", this.keyDown);
                window.removeEventListener("keyup", this.keyUp);
                clearInterval(intervalId);
                this.isNotConnected = true;
                if (event.wasClean) {
                    console.log(
                        `[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`
                    );
                } else {
                    console.log("[close] Соединение прервано");
                }
            };
            this.socket.onerror = () => {
                this.showNegNotify("Ошибка соединения");
                this.isNotConnected = true;
                clearInterval(intervalId);
            };
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
<style>
.img-m {
    width: 640px;
    height: 480px;
}

.arrow {
    text-align: center;
}

.arrow-down {
    transform: rotate(180deg);
}

.arrow-right {
    transform: rotate(270deg);
}

.arrow-left {
    transform: rotate(90deg);
}

.arrow-holder {
    max-width: 129px;
    align-self: center;
}
</style>
