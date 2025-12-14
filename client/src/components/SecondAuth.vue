<script setup>
import {ref, watch} from 'vue';
import axios from 'axios';
import { useUserInfoStore } from '@/stores/user_info_store';
import QRCode from 'qrcode'
const key = ref();

const userInfoStore = useUserInfoStore();
const totpUrl = ref();
const qrcodeUrl = ref();

watch(totpUrl, async () => {
    qrcodeUrl.value = await QRCode.toDataURL(totpUrl.value);
})

async function onActivate() {
    await axios.post("/api/users/second-login/", {
        key: key.value
    })
    await userInfoStore.fetchUserInfo();
}

async function getTotpKey() {
    let r = await axios.get('/api/users/get-totp/')
    totpUrl.value = r.data.url;
}


async function onCreateGroup() {
    await axios.post("/api/students/create-custom-group/")
}
</script>


<template> 
    <input type="text" v-model="key">
    <button @click="onActivate">Активровать второй фактор</button>
    <button @click="onCreateGroup">Создать группу</button>
    <br>
    <button @click="getTotpKey">Запросить ключ</button>
    <br>
    <div style="padding: 1rem  0">{{ totpUrl  }}</div>
    <br>
    <img :src="qrcodeUrl" alt="">
</template>