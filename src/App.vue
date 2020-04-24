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
                            <img :src="mainImg" class="img-m" />
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
            </q-page>
        </q-page-container>
    </q-layout>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";

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
            intervalId: null,
            leftDrawerOpen: false,
            isNotConnected: true,
            ipText: "127.0.0.1",
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
        /**
         * Метод для обработки нажатия кнопки возврата к настройкам
         */
        getBackToSetting() {
            this.socket.close();
        },

        /**
         * Метод показывает важные уведомления (ошибки и проч.)
         * parms: outMsg - сообщение уведомления
         */
        showNegNotify(outMsg) {
            this.$q.notify({
                type: "negative",
                message: outMsg,
            });
        },

        /**
         * Метод обработки нажатия на кнопку "Подключиться"
         */
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

        /**
         * Обрабатывает события нажатия на стрелки клавиатуры
         */
        keyDown(e) {
            /**
             * Если код нажатой клавиши соответствует нужной, тогда сигнализируем, что она была нажата,
             * а цвет иконки изменяем.
             */
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

        /**
         * Обработчик отжатия клавиш стрелок
         */
        keyUp(e) {
            // Если код клавиши соответсвует, то сигнализируется отжатие, а цвет иконки изменяется
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

        /**
         * Метод, настраивающий соединение с сервером
         */
        socketSetting() {
            try {
                // Пытаемся соединиться с сервером через сокет
                this.socket = new WebSocket(
                    "ws://" + this.ipText + ":" + this.portText
                );

                // Добавляем обработчики событий
                this.socket.onopen = () => {
                    /**
                     * При удачном соединении открывается экран управления,
                     * добавляеются обработчики событий нажатия на стрелки и
                     * устанавливается интервал отправки сообщений
                     */
                    this.isNotConnected = false;
                    window.addEventListener("keydown", this.keyDown);
                    window.addEventListener("keyup", this.keyUp);
                    this.intervalId = setInterval(this.sendingMessage, 100);
                };
                this.socket.onmessage = (event) => {
                    this.mainImg = "data:image/jpg;base64, " + event.data;
                };
                this.socket.onclose = () => {
                    /**
                     * При закрытии сокета:
                     *      1. удаляем слушателей событий;
                     *      2. удаляем интервал;
                     *      3. показваем окно настройки соединения;
                     *      4. показываем уведомление пользователю
                     */
                    window.removeEventListener("keydown", this.keyDown);
                    window.removeEventListener("keyup", this.keyUp);
                    clearInterval(this.intervalId);
                    this.isNotConnected = true;
                    this.showNegNotify("Соединение закрыто");
                };
                this.socket.onerror = () => {
                    this.showNegNotify("Ошибка соединения");
                    this.isNotConnected = true;
                    clearInterval(this.intervalId);
                };
            } catch (e) {
                // При неудачном соединении показывается уведомление
                this.showNegNotify(
                    "Ошибка соединения, проверьте правильность введенных данных"
                );
            }
        },

        /**
         * Метод отправки сообщения серверу
         */
        sendingMessage() {
            // velocity(left, right) pid ml
            /**
             * Скорости для левых и правых колес
             * Скорость = [1; 0], 1 - максимальная, 0 - колеса не крутятся
             * При умножении на -1 - крутятся в обратную сторону
             */
            let rightSpeed = 0;
            let leftSpeed = 0;

            // Выходное сообщение: {скорость левых колес} {скорость правых колес} {используем ПИД?} {используем распознование лиц?}
            let outMessage = "";

            // Формируем направление движения от логических переменных нажатия кнопок
            if (this.keyUpPressed) (leftSpeed = 1), (rightSpeed = 1);
            if (this.keyDownPressed) (leftSpeed = -1), (rightSpeed = -1);
            if (this.keyLeftPressed) rightSpeed = 1;
            if (this.keyRightPressed) leftSpeed = 1;

            outMessage = leftSpeed + " " + rightSpeed + " ";
            // Добавляем к сообщению данные о включенных опциях
            if (this.usePID) outMessage += 1;
            else outMessage += 0;
            if (this.useML) outMessage += " " + 1;
            else outMessage += " " + 0;

            // Отправляем сообщение
            this.socket.send(outMessage);
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
