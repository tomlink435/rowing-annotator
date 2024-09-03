import { createApp } from 'vue'
import ElementPlus, {ElMessage, Table} from 'element-plus'
import App from './App.vue'
import router from './router/index'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'element-plus/dist/index.css'
import store from './store/index'
import { createPinia } from 'pinia';
import {usePermissStore} from "@/store/permiss";
import 'vue3-video-play/dist/style.css'

const app = createApp(App).use(store)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}



//拦截处理交互信息
axios.interceptors.response.use(function(response){
    const res = response.data;

    if(res.code === 200){
        return res.data;
    }else if(res.code === 302){
        window.location.href = '/login';
        return Promise.reject(res);
    }else{
        ElMessage.warning(res.message)
        return res.code;
    }
},(error)=>{
    ElMessage.error(error.message);
    return Promise.reject(error);
});

app.use(router)
app.use(store)
app.use(VueAxios,axios);
app.use(ElementPlus)
app.use(createPinia())

const permiss = usePermissStore();
app.directive('permiss', {
    mounted(el, binding) {
        if (!permiss.key.includes(String(binding.value))) {
            el['hidden'] = true;
        }
    },
});
app.mount('#app')

