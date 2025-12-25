import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router'; 
import Cookies from 'js-cookie';
import { onBeforeMount, ref } from "vue"; 

export const useUserInfoStore = defineStore("userInfoStore", () => {

    const username = ref();
    const is_authenticated = ref(null);
    const permissions = ref([])
    //const can_see_page2 = ref(false);
    const second = ref(null);
    async function fetchUserInfo() {
        const r = await axios.get("/api/users/my/");
        //userInfo.value=r.data; 
        username.value = r.data.username;
        is_authenticated.value = r.data.is_authenticated;
        permissions.value = r.data.permissions;
        second.value = r.data.second;
        //can_see_page2.value = r.data.can_see_page2;

        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    }

    function hasPermission(name) {
        return permissions.value.includes(name);
    }
    
    onBeforeMount(async () => {
        
        fetchUserInfo();
    })

    return {
        username,
        is_authenticated,
        permissions,
        second,
        //can_see_page2, 
        fetchUserInfo,
        hasPermission,
    }

});