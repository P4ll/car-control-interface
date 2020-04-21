<template>
    <q-page class="flex flex-center">
        <q-list>
            <q-item>
                <img src="../assets/block.jpg" alt="Страница не найдена, 404" clickable/>
            </q-item>
            <q-item>
                <q-btn label="На начальную страницу" @click="getBack" />
            </q-item>
        </q-list>
    </q-page>
</template>
<script>
export default {
    name: "ErrorPage",
    methods: {
        getBack() {},
    },
};
</script>
<style></style>
