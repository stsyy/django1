<script setup>
import {ref, watch} from 'vue';
import axios from 'axios';
import { useUserInfoStore } from '@/stores/user_store';
import QRCode from 'qrcode';
import { onMounted } from 'vue';
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
    },{withCredentials:true});
    await userInfoStore.fetchUserInfo();

}

async function getTotpKey() {
    let r = await axios.get('/api/users/get-totp/')
    totpUrl.value = r.data.url;
}



</script>


<template> 
    <input type="text" v-model="key">
    <button @click="onActivate">Активровать второй фактор</button>
    
    <br>
    <button @click="getTotpKey">Запросить ключ</button>
    <br>
    <div style="padding: 1rem  0">{{ totpUrl  }}</div>
    <br>
    <img :src="qrcodeUrl" alt="">
</template>